from django.conf import settings
from companies.controllers import CompaniesController

class CompanyDetectionMiddleware(object):
    def process_request(self, request):
        if 'company_id' in request.GET:
            company_id = request.GET['company_id']
        else:
            path_parts = [p for p in request.get_full_path().split('/') if p]
            if len(path_parts) < 2:
                request.company = None
                return
            if path_parts[0] != settings.SITE_URLS['company_prefix']:
                request.company = None
                return
            company_id = path_parts[1]
        company = CompaniesController.GetCompanyById(company_id)
        request.company = company
