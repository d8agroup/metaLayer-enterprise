from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^admin/', include('enterprise.admin.urls')),
    url(r'', include('enterprise.themanager.urls')),
)
