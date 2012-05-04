from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from companies.controllers import  ProjectsController, CompaniesController, ActivityRecordsController
import constants
from customtags.templatetags.custom_tags import is_company_admin
from metalayercore.actions.controllers import ActionController
from metalayercore.dashboards.controllers import DashboardsController
from metalayercore.datapoints.controllers import DataPointController
from metalayercore.outputs.controllers import OutputController
from metalayercore.visualizations.controllers import VisualizationController
from themanager.forms import login_form_is_valid
from themanager.utils import render_to_device, ensure_company_membership
from userprofiles.controllers import UserController
from enterprise.utils import JSONResponse

def landing_page(request):
    template_data = {}
    if request.method == 'POST':
        passed, errors = login_form_is_valid(request)
        if passed:
            passed, errors, redirect = UserController.UserCanBeLoggedInAndRedirected(
                request,
                request.POST['username'],
                request.POST['password'],
            )
            if passed:
                user = UserController.GetUserByEmail(request.POST['username'])
                ActivityRecordsController.RecordLogin(user, CompaniesController.IdentifyCompanyForUser(user))
                return redirect
        template_data['login_form'] = {
            'errors':errors,
            'username':request.POST.get('username')
        }
    return render_to_device(request, template_data, '/themanager/login.html')

def logout(request):
    UserController.LogoutUser(request)
    return redirect(landing_page)

@ensure_company_membership
def company_root(request):
    template_data = {
        'projects':ProjectsController.GetCompanyProjectsForUser(request.company, request.user),
        'company_activity':ActivityRecordsController.GetAndFormatCompanyWideActivity(request.user, request.company)
    }
    return render_to_device(
        request,
        template_data,
        '/themanager/company_home.html'
    )

@ensure_company_membership
def new_project(request):
    ActivityRecordsController.RecordProjectCreated(request.user, request.company)
    project = ProjectsController.CreateNewProjectInCompany(request.company)
    return redirect('/%s/%s/projects/edit/%s' % (settings.SITE_URLS['company_prefix'], request.company.id, project.project_id))

@ensure_company_membership
def edit_project(request, id):
    template_data = {
        'company_members':[UserController.GetUserByUserId(c) for c in request.company.members],
        'data_points':[DataPointController.LoadDataPoint(d).get_unconfigured_config() for d in request.company.data_points_available],
        'actions':[ActionController.LoadAction(a).get_unconfigured_config() for a in request.company.actions_available],
        'outputs':[OutputController.LoadOutput(o).get_unconfigured_config() for o in request.company.outputs_available],
        'visualizations':[VisualizationController.LoadVisualization(v).get_unconfigured_config() for v in request.company.visualizations_available],
    }
    project = ProjectsController.GetProjectById(request.company, request.user, id)
    if not project:
        messages.error(request, constants.TEMPLATE_STRINGS['view_project']['message_not_project_member'])
        return redirect('/%s/%s' % (settings.SITE_URLS['company_prefix'], request.company.id))

    if request.method == 'POST' and request.POST.get('delete'):
        ProjectsController.MarkProjectAsInactive(request.company, id)
        messages.info(request, constants.TEMPLATE_STRINGS['manage_project']['message_project_inactive'] % project.display_name)
        return redirect('/%s/%s' % (settings.SITE_URLS['company_prefix'], request.company.id))
    elif request.method == 'POST':
        passed, errors = ProjectsController.UpdateProjectFromFormValues(id, request.company, request.POST)
        if passed:
            ActivityRecordsController.RecordProjectSaved(request.user, request.company, project)
            messages.info(request, constants.TEMPLATE_STRINGS['manage_project']['message_project_saved'] % request.POST['display_name'])
            return redirect('/%s/%s' % (settings.SITE_URLS['company_prefix'], request.company.id))
        template_data['errors'] = errors
        template_data['project'] = request.POST
    else:
        template_data['project'] = project
    return render_to_device(
        request,
        template_data,
        '/themanager/project_edit.html'
    )

@ensure_company_membership
def view_project(request, project_id):
    if 'delete_insight' in request.GET:
        delete_insight = request.GET.get('delete_insight')
        insight = DashboardsController.GetDashboardById(delete_insight)
        if insight and (is_company_admin(request.user, request.company) or request.user.username == insight.username):
            DashboardsController.DeleteDashboardById(delete_insight)
            messages.info(request, constants.TEMPLATE_STRINGS['view_project']['message_insight_deleted'])

    template_data = {
        'project':ProjectsController.GetProjectById(request.company, request.user, project_id),
        'project_activity':ActivityRecordsController.GetAndFormatProjectWideActivity(request.user, request.company, project_id)
    }

    if not template_data['project']:
        raise Http404

    template_data['project_members'] = [UserController.GetUserByUserId(u) for u in request.company.administrators] + [UserController.GetUserByUserId(u) for u in template_data['project'].members]
    template_data['project_insights'] = sorted([i for i in [DashboardsController.GetDashboardById(d) for d in template_data['project'].insights] if i['active'] == True and i['deleted'] == False], key=lambda db: db.last_saved, reverse=True)

    return render_to_device(
        request,
        template_data,
        '/themanager/project_view.html'
    )

@ensure_company_membership
def create_project_insight(request, project_id):
    project = ProjectsController.GetProjectById(request.company, request.user, project_id)

    if not project:
        raise Http404

    dc = DashboardsController(request.user)
    db = dc.create_new_dashboard_from_template(1)
    ActivityRecordsController.RecordInsightCreated(request.user, request.company, project)
    ProjectsController.AddInsightToProject(request.company, project.project_id, db.id)
    return redirect('/dashboard/%s?next=/%s/%s/projects/%s&company_id=%s&project_id=%s' % (db.id, settings.SITE_URLS['company_prefix'], request.company.id, project_id, request.company.id, project_id))

@ensure_company_membership
def load_project_insight(request, project_id, insight_id):
    project = ProjectsController.GetProjectById(request.company, request.user, project_id)

    if not project:
        raise Http404

    db = DashboardsController.GetDashboardById(insight_id)
    if db.username == request.user.username:
        ActivityRecordsController.RecordInsightEdited(request.user, request.company, project, db)
        return redirect('/dashboard/%s?next=/%s/%s/projects/%s&company_id=%s&project_id=%s' % (db.id, settings.SITE_URLS['company_prefix'], request.company.id, project_id, request.company.id, project_id))

    ActivityRecordsController.RecordInsightRemixed(request.user, request.company, project, db)
    dc = DashboardsController(request.user)
    db = dc.create_new_dashboard_from_dashboard(insight_id)
    ProjectsController.AddInsightToProject(request.company, project.project_id, db.id)
    return redirect('/dashboard/%s?next=/%s/%s/projects/%s&company_id=%s&project_id=%s' % (db.id, settings.SITE_URLS['company_prefix'], request.company.id, project_id, request.company.id, project_id))

@ensure_company_membership
def load_project_widgets(request):
    project = ProjectsController.GetProjectById(request.company, request.user, request.GET['project_id'])

    if not project:
        raise Http404
    return_data = {
        'data_points':[DataPointController.LoadDataPoint(d).get_unconfigured_config() for d in project.data_points_available],
        'actions':[ActionController.LoadAction(a).get_unconfigured_config() for a in project.actions_available],
        'outputs':[OutputController.LoadOutput(o).get_unconfigured_config() for o in project.outputs_available],
        'visualizations':[VisualizationController.LoadVisualization(v).get_unconfigured_config() for v in project.visualizations_available],
    }
    return JSONResponse(return_data)

def load_project_api_keys(request):
    api_keys = [{
        'name':k['type'],
        'display_name':k['display_name'],
        'api_key':k['api_key'],
        'help_text':k['help']
    } for k in CompaniesController.GetCompanyAPIKeys(request.company.id)]
    return JSONResponse({ 'api_keys':api_keys })

@ensure_company_membership
def edit_user(request, id=None):
    template_data = {}
    if request.method == 'POST':
        passed, errors = UserController.CreateNewUserFromValues(request.POST, request.company)
        if passed:
            user = UserController.GetUserByEmail(request.POST['email'])
            CompaniesController.AddUserToCompany(request.company, user)
            if id:
                message_key = 'message_user_saved'
                ActivityRecordsController.RecordUserSaved(request.user, request.company, secondary_user=user)
            else:
                message_key = 'message_user_created'
                ActivityRecordsController.RecordUserCreated(request.user, request.company, secondary_user=user)
            messages.info(request, constants.TEMPLATE_STRINGS['manage_user'][message_key] % request.POST['email'])
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            return redirect('/%s/%s' % (settings.SITE_URLS['company_prefix'], request.company.id))
        template_data['errors'] = errors
        template_data['subject_user'] = request.POST
    else:
        template_data['subject_user'] = UserController.GetUserByUserId(id) if id else None
    return render_to_device(
        request,
        template_data,
        '/themanager/user_edit.html'
    )

