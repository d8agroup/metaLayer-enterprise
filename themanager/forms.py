from django.template.defaultfilters import escape
import constants

def login_form_is_valid(request):
    if not request.POST:
        return False, []
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        return False, [constants.TEMPLATE_STRINGS['login']['form_errors_no_username_or_password']]
    return True, []

def clean_and_validate_project_form(values):
    clean_values = {
        'display_name':escape(values['display_name']),
        'description':escape(values['description']),
        'active':False if 'active' in values and values['active'] == 'False' else True,
        'members':values.getlist('members') if 'members' in values else []
    }
    errors = []
    if not clean_values['display_name']:
        errors.append(constants.TEMPLATE_STRINGS['manage_project']['form_errors_display_name'])
    if not clean_values['description']:
        errors.append(constants.TEMPLATE_STRINGS['manage_project']['form_errors_description'])

    return len(errors) == 0, errors, clean_values