from django.conf.urls.defaults import patterns, include, url
from enterprise.admin.views import *

urlpatterns = patterns('',
    url(r'companies/(\w+)/delete$', delete_company),
    url(r'companies/(\w+)$', companies),
    url(r'users/(\w+)$', users),
    url(r'users$', users),
    url(r'$', home),
)
