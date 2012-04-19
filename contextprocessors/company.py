from django.conf import settings
from companies.controllers import CompaniesController

def context_company(request):
    company = _get_company_from_url(request)

    if not company:
        company = _get_company_from_user(request)

    if not company:
        return {}

    return {
        'company':company
    }

def _get_company_from_url(request):
    path_parts = [p for p in request.get_full_path().split('/') if p]
    if len(path_parts) < 2:
        return None
    if path_parts[0] != settings.SITE_URLS['company_prefix']:
        return None
    company_id = path_parts[1]
    company = CompaniesController.GetCompanyById(company_id)
    return company

def _get_company_from_user(request):
    user = request.user
    if not user:
        return None
    company = CompaniesController.IdentifyCompanyForUser(user)
    if not company:
        return None
    return company

