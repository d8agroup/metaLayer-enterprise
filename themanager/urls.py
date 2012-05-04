from django.conf.urls.defaults import patterns, url
from themanager.views import *

urlpatterns = patterns('',
    url(r'%s/\w+$' % settings.SITE_URLS['company_prefix'], company_root),
    url(r'%s/\w+/projects/new$' % settings.SITE_URLS['company_prefix'], new_project),
    url(r'%s/\w+/projects/edit/(\w+)$' % settings.SITE_URLS['company_prefix'], edit_project),
    url(r'%s/\w+/projects/(\w+)/dashboard$' % settings.SITE_URLS['company_prefix'], create_project_insight),
    url(r'%s/\w+/projects/(\w+)/dashboard/(\w+)$' % settings.SITE_URLS['company_prefix'], load_project_insight),
    url(r'%s/\w+/projects/(\w+)/get_widgets$' % settings.SITE_URLS['company_prefix'], load_project_widgets),
    url(r'%s/\w+/projects/(\w+)$' % settings.SITE_URLS['company_prefix'], view_project),
    url(r'%s/\w+/users/new$' % settings.SITE_URLS['company_prefix'], edit_user),
    url(r'%s/\w+/users/edit/(\w+)$' % settings.SITE_URLS['company_prefix'], edit_user),
    url(r'%s/\w+/change_password$' % settings.SITE_URLS['company_prefix'], change_password),
    url(r'%s/\w+/logout$' % settings.SITE_URLS['company_prefix'], logout),
    url(r'logout$', logout),
    url(r'$', landing_page),
)
