from companies.controllers import CompaniesController, ProjectsController
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
