from django.conf import settings
from django.shortcuts import redirect
from companies.controllers import CompaniesController

def process_login_and_get_redirect(request, user):
    """
    Providentia users (not admins) are redirected to the welcome screen.
    
    """
    
    if not user:
        return None
    company = CompaniesController.IdentifyCompanyForUser(user)
    if not company:
        return None
    
    if not company.projects or len(company.projects) == 0:
        return None
    
    project = company.projects[0]
    
    return redirect('/%s/%s/projects/%s' % (settings.SITE_URLS['company_prefix'], company.id, project.project_id))