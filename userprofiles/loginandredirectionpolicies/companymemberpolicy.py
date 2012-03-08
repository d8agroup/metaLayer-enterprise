from django.conf import settings
from django.shortcuts import redirect
from companies.controllers import CompaniesController

def process_login_and_get_redirect(request, user):
    if not user:
        return None
    company = CompaniesController.IdentifyCompanyForUser(user)
    if not company:
        return None
    return redirect('/%s/%s' % (settings.SITE_URLS['company_prefix'], company.id))