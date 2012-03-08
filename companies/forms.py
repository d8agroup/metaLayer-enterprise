from django.template.defaultfilters import escape
import constants

def validate_company(company_id, values):
    return_values = {
        'display_name': escape(values['display_name']),
        'administrators':values.getlist('administrators') if 'administrators' in values else [],
    }
    for key in ['data_points_available', 'actions_available', 'outputs_available', 'visualizations_available']:
        if key in values:
            return_values[key] = values.getlist(key)
    if not return_values['display_name'] or return_values['display_name'] == constants.MODEL_DEFAULTS['companies']['default_display_name']:
        return False, [constants.TEMPLATE_STRINGS['manage_company']['form_error_display_name']], values

    from enterprise.companies.controllers import CompaniesController

    existing_company = CompaniesController.GetCompanyByDisplayName(return_values['display_name'])
    if existing_company and existing_company.id != company_id:
        return False, [constants.TEMPLATE_STRINGS['manage_company']['form_error_display_name_used']], values

    return True, [], return_values

def clean_and_validate_project_form(values):
    clean_values = {
        'display_name':escape(values['display_name']),
        'description':escape(values['description']),
        'active':False if 'active' in values and values['active'] == 'False' else True,
        'members':values.getlist('members') if 'members' in values else []
    }
    for key in ['data_points_available', 'actions_available', 'outputs_available', 'visualizations_available']:
        if key in values:
            clean_values[key] = values.getlist(key)
    errors = []
    if not clean_values['display_name']:
        errors.append(constants.TEMPLATE_STRINGS['manage_project']['form_errors_display_name'])
    if not clean_values['description']:
        errors.append(constants.TEMPLATE_STRINGS['manage_project']['form_errors_description'])

    return len(errors) == 0, errors, clean_values