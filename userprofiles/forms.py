from django.core.validators import email_re
from django.template.defaultfilters import escape
import re
import constants

def validate_user(values):
    return_values = {
        'email':escape(values['email']),
        'username':escape(values['email']),
        'first_name':escape(values['first_name']) if 'first_name' in values else None,
        'last_name':escape(values['last_name']) if 'last_name' in values else None,
        'is_staff':values['is_staff'] if 'is_staff' in values else False,
    }
    errors = []
    if not email_re.search(return_values['email']):
        errors.append(constants.TEMPLATE_STRINGS['manage_user']['form_error_email_regex'])
    if return_values['first_name'] and not re.search(r'^\w+$', return_values['first_name']):
        errors.append(constants.TEMPLATE_STRINGS['manage_user']['form_error_first_name'])
    if return_values['last_name'] and not re.search(r'^\w+$', return_values['last_name']):
        errors.append(constants.TEMPLATE_STRINGS['manage_user']['form_error_last_name'])

    if errors:
        return False, errors, None
    return True, [], return_values