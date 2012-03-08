from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from companies.controllers import  ProjectsController, CompaniesController
import constants
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
        'projects':ProjectsController.GetCompanyProjectsForUser(request.company, request.user)
    }
    return render_to_device(
        request,
        template_data,
        '/themanager/company_home.html'
    )

@ensure_company_membership
def new_project(request):
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

    if request.method == 'POST':
        passed, errors = ProjectsController.UpdateProjectFromFormValues(id, request.company, request.POST)
        if passed:
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
    template_data = {
        'project':ProjectsController.GetProjectById(request.company, request.user, project_id)
    }

    if not template_data['project']:
        raise Http404

    template_data['project_members'] = [UserController.GetUserByUserId(u) for u in template_data['project'].members]
    template_data['project_insights'] = [i for i in [DashboardsController.GetDashboardById(d) for d in template_data['project'].insights] if i['active'] == True and i['deleted'] == False]

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
    ProjectsController.AddInsightToProject(request.company, project.project_id, db.id)
    return redirect('/dashboard/%s?next=/%s/%s/projects/%s&company_id=%s&project_id=%s' % (db.id, settings.SITE_URLS['company_prefix'], request.company.id, project_id, request.company.id, project_id))

@ensure_company_membership
def load_project_insight(request, project_id, insight_id):
    project = ProjectsController.GetProjectById(request.company, request.user, project_id)

    if not project:
        raise Http404

    db = DashboardsController.GetDashboardById(insight_id)
    if db.username == request.user.username:
        return redirect('/dashboard/%s?next=/%s/%s/projects/%s&company_id=%s&project_id=%s' % (db.id, settings.SITE_URLS['company_prefix'], request.company.id, project_id, request.company.id, project_id))

    dc = DashboardsController(request.user)
    db = dc.create_new_dashboard_from_dashboard(insight_id)
    ProjectsController.AddInsightToProject(request.company, project.project_id, db.id)
    return redirect('/dashboard/%s?next=/%s/%s/projects/%s&company_id=%s&project_id=%s' % (db.id, settings.SITE_URLS['company_prefix'], request.company.id, project_id, request.company.id, project_id))


@ensure_company_membership
def load_project_widgets(request, project_id):
    project = ProjectsController.GetProjectById(request.company, request.user, project_id)

    if not project:
        raise Http404
    return_data = {
        'data_points':[DataPointController.LoadDataPoint(d).get_unconfigured_config() for d in request.company.data_points_available],
        'actions':[ActionController.LoadAction(a).get_unconfigured_config() for a in request.company.actions_available],
        'outputs':[OutputController.LoadOutput(o).get_unconfigured_config() for o in request.company.outputs_available],
        'visualizations':[VisualizationController.LoadVisualization(v).get_unconfigured_config() for v in request.company.visualizations_available],
    }
    return JSONResponse(return_data)

@ensure_company_membership
def edit_user(request, id=None):
    template_data = {}
    if request.method == 'POST':
        passed, errors = UserController.CreateNewUserFromValues(request.POST, request.company)
        if passed:
            user = UserController.GetUserByEmail(request.POST['email'])
            CompaniesController.AddUserToCompany(request.company, user)
            message_key = 'message_user_saved' if id else 'message_user_created'
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

