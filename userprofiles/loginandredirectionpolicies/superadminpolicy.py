from django.shortcuts import redirect
from enterprise.admin.views import home

def process_login_and_get_redirect(request, user):
    if not user:
        return None
    if not user.is_staff:
        return None
    return redirect(home)