from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
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
        'users': users
    }

    if request.method == 'POST':
        passed, errors = CompaniesController.UpdateCompanyFromFormValues(id, request.POST)
        if passed:
            messages.info(request, 'Company updated successfully')
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
