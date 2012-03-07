from django.conf import settings
from django.conf.urls.defaults import patterns, url
from themanager.views import *

urlpatterns = patterns('',
    url(r'%s/\w+$' % settings.SITE_URLS['company_prefix'], company_root),
    url(r'$', landing_page)
)
