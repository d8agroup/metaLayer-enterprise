from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.functional import wraps

def template_for_device(request, template_path):
    return '%s%s' % (request.device_context, template_path)

def render_to_device(request, template_data, template_path):
    return render_to_response(
        template_for_device(request, template_path),
        template_data,
        context_instance=RequestContext(request)
    )

def ensure_company_membership(func):
    def inner_func(request, *args, **kwargs):
        user = request.user
        company = request.company
        if not user.is_staff and user.id not in company.administrators and user.id not in company.members:
            raise Http404
        return func(request, *args, **kwargs)
    return wraps(func)(inner_func)