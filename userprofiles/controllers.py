import random
import string
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import constants
from emails.controllers import EmailController
from userprofiles.forms import validate_user
from utils import dynamic_import

class UserController(object):
    @classmethod
    def UserCanBeLoggedInAndRedirected(cls, request, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            return False, [constants.TEMPLATE_STRINGS['login']['form_errors_incorrect_username_or_password']], None
        elif not user.is_active:
            return False, [constants.TEMPLATE_STRINGS['login']['form_errors_user_inactive']], None
        login(request, user)

        for policy in settings.LOGIN_AND_REDIRECTION_POLICIES:
            policy_module = dynamic_import('enterprise.userprofiles.loginandredirectionpolicies.%s' % policy)
            policy_function = getattr(policy_module, 'process_login_and_get_redirect')
            user_redirect = policy_function(request, user)
            if user_redirect:
                return True, [], user_redirect

        return False, [constants.TEMPLATE_STRINGS['login']['form_errors_user_type_not_supported']], None

    @classmethod
    def CreateNewUserFromValues(cls, values):
        passed, errors, clean_values = validate_user(values)
        if not passed:
            return False, errors

        if User.objects.filter(username=clean_values['username']).count():
            return False, [constants.TEMPLATE_STRINGS['manage_user']['form_error_user_exists']]

        user_password = "".join([random.choice(string.letters) for i in xrange(6)])
        user = User.objects.create_user(clean_values['username'], clean_values['username'], user_password)
        if clean_values['first_name']:
            user.first_name = clean_values['first_name']
        if clean_values['last_name']:
            user.last_name = clean_values['last_name']
        user.save()

        email_controller = EmailController()
        email_controller.send_new_user_created_email(user, user_password)
        return True, []

    @classmethod
    def GetUserByUserId(cls, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return None
        return user

