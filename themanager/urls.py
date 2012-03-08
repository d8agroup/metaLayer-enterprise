from django.conf.urls.defaults import patterns, url
from themanager.views import *

urlpatterns = patterns('',
    url(r'%s/\w+$' % settings.SITE_URLS['company_prefix'], company_root),
    url(r'%s/\w+/projects/new$' % settings.SITE_URLS['company_prefix'], new_project),
    url(r'%s/\w+/projects/edit/(\w+)$' % settings.SITE_URLS['company_prefix'], edit_project),
    url(r'%s/\w+/projects/(\w+)$' % settings.SITE_URLS['company_prefix'], view_project),
    url(r'%s/\w+/users/new$' % settings.SITE_URLS['company_prefix'], edit_user),
    url(r'%s/\w+/users/edit/(\w+)$' % settings.SITE_URLS['company_prefix'], edit_user),
    url(r'logout$', logout),
    url(r'$', landing_page),
)
