from django.conf.urls.defaults import patterns, include, url
from themanager.views import load_project_widgets, load_project_api_keys

urlpatterns = patterns('',
    #Special rules to overload the normal dashboard functions
    url(r'dashboard/widgets/get_all', load_project_widgets),
    url(r'dashboard/api_keys/load', load_project_api_keys),

    url(r'^aggregation/', include('metalayercore.aggregator.urls')),
    url(r'^admin/', include('enterprise.admin.urls')),
    url(r'^dashboard/', include('enterprise.thedashboard.urls')),
    url(r'^i/', include('metalayercore.imaging.urls')),
    url(r'^o/', include('metalayercore.outputs.urls')),
    url(r'^u/', include('metalayercore.datauploader.urls')),
    url(r'^oauth2/', include('metalayercore.oauth2bridge.urls')),
    url(r'', include('enterprise.themanager.urls')),
)
