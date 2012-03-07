from django.template.defaultfilters import escape
import constants

def validate_company(company_id, values):
    return_values = {
        'display_name': escape(values['display_name']),
        'administrators':values.getlist('administrators') if 'administrators' in values else [],
    }
    if not return_values['display_name'] or return_values['display_name'] == constants.MODEL_DEFAULTS['companies']['default_display_name']:
        return False, [constants.TEMPLATE_STRINGS['manage_company']['form_error_display_name']], values

    from enterprise.companies.controllers import CompaniesController

    existing_company = CompaniesController.GetCompanyByDisplayName(return_values['display_name'])
    if existing_company and existing_company.id != company_id:
        return False, [constants.TEMPLATE_STRINGS['manage_company']['form_error_display_name_used']], values

    return True, [], return_values