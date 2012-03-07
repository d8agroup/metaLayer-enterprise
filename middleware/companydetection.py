from django.conf import settings
from companies.controllers import CompaniesController

class CompanyDetectionMiddleware(object):
    def process_request(self, request):
        path_parts = [p for p in request.get_full_path().split('/') if p]
        if len(path_parts) < 2:
            return
        if path_parts[0] != settings.SITE_URLS['company_prefix']:
            return
        company_id = path_parts[1]
        company = CompaniesController.GetCompanyById(company_id)
        request.company = company
