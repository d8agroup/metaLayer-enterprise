import constants

def login_form_is_valid(request):
    if not request.POST:
        return False, []
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        return False, [constants.TEMPLATE_STRINGS['login']['form_errors_no_username_or_password']]
    return True, []
