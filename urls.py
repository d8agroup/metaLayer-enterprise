from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^admin/', include('enterprise.admin.urls')),
    url(r'^dashboard/', include('enterprise.thedashboard.urls')),
    url(r'^i/', include('enterprise.imaging.urls')),
    url(r'', include('enterprise.themanager.urls')),
)
