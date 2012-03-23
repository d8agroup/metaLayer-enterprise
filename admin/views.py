from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from admin.utils import get_all_available_data_points, get_all_available_actions, get_all_available_outputs, get_all_available_visualizations
from companies.controllers import CompaniesController
from userprofiles.controllers import UserController

def home(request):
    template_data = {
        'companies': CompaniesController.GetAllCompanies()
    }
    return render_to_response(
        'web/admin/home.html',
        template_data,
        context_instance=RequestContext(request)
    )

def companies(request, id):
    if id == 'new':
        company = CompaniesController.CreateNewEmptyCompany()
        return redirect(companies, company.id)

    company = CompaniesController.GetCompanyById(id)

    users = User.objects.filter(is_active=True, is_staff=False)
    sorted(users, key=lambda u: u.id in company.administrators)

    template_data = {
        'users': users,
        'data_points':[d.get_unconfigured_config() for d in get_all_available_data_points()],
        'actions':[a.get_unconfigured_config() for a in get_all_available_actions()],
        'outputs':[o.get_unconfigured_config() for o in get_all_available_outputs()],
        'visualizations':[v.get_unconfigured_config() for v in get_all_available_visualizations()],
    }

    if request.method == 'POST':
        passed, errors = CompaniesController.UpdateCompanyFromFormValues(id, request.POST)
        if passed:
            messages.info(request, 'Company updated successfully')
            if CompaniesController.GetCompanyAPIKeys(id):
                messages.info(request, 'You can now set company level api keys')
                return redirect(api_keys, id)
            return redirect(home)
        template_data['company'] = request.POST
        template_data['errors'] = errors
    else:
        template_data['company'] = company
    return render_to_response(
        'web/admin/company.html',
        template_data,
        context_instance=RequestContext(request)
    )

def delete_company(request, id):
    company = CompaniesController.GetCompanyById(id)
    if request.method == 'POST':
        CompaniesController.DeleteCompanyById(id)
        messages.info(request, 'Company successfully deleted.')
        return redirect(home)
    template_data = {
        'company':company
    }
    return render_to_response(
        'web/admin/company_delete.html',
        template_data,
        context_instance=RequestContext(request)
    )

def api_keys(request, id):
    company = CompaniesController.GetCompanyById(id)
    if not company:
        messages.error(request, 'Sorry, something went wrong loading the company with id: %s' % id)
        return redirect(home)

    if request.method == 'POST':
        CompaniesController.UpdateCompanyAPIKeysFromFormValues(id, request.POST)
        messages.info(request, 'Api Keys Saved')
        return redirect(home)

    template_data = {
        'api_keys':CompaniesController.GetCompanyAPIKeys(id)
    }

    return render_to_response(
        'web/admin/api_keys.html',
        template_data,
        context_instance=RequestContext(request)
    )

def users(request, id):
    template_data = {}
    if request.method == 'POST':
        passed, errors = UserController.CreateNewUserFromValues(request.POST)
        if passed:
            return redirect(request.GET.get('next') or home)
        template_data['errors'] = errors
        template_data['user'] = request.POST
    else:
        template_data['user'] = UserController.GetUserByUserId(id) if id and not id == 'new' else None
    return render_to_response(
        'web/admin/user.html',
        template_data,
        context_instance=RequestContext(request)
    )
