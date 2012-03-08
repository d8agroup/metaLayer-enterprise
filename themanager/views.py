from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from companies.controllers import  ProjectsController, CompaniesController
import constants
from themanager.forms import login_form_is_valid
from themanager.utils import render_to_device, ensure_company_membership
from userprofiles.controllers import UserController

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
        'company_members':[UserController.GetUserByUserId(c) for c in request.company.members]
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

    return render_to_device(
        request,
        template_data,
        '/themanager/project_view.html'
    )

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

