from django.conf import settings
from django.template.loader import render_to_string

def context_additionalhtml(request):
    try:
        additional_page_includes = getattr(settings, 'ADDITIONAL_PAGE_INCLUDES')
        additional_html = ''.join([render_to_string(page) for page in additional_page_includes])
    except AttributeError:
        additional_html = ''

    return {
        'additional_html':additional_html
    }