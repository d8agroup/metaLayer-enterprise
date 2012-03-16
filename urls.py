from django.conf.urls.defaults import patterns, include, url
from themanager.views import load_project_widgets

urlpatterns = patterns('',
    #Special rules to overload the normal dashboard functions
    url(r'dashboard/widgets/get_all', load_project_widgets),

    url(r'^aggregation/', include('metalayercore.aggregator.urls')),
    url(r'^admin/', include('enterprise.admin.urls')),
    url(r'^dashboard/', include('enterprise.thedashboard.urls')),
    url(r'^i/', include('enterprise.imaging.urls')),
    url(r'', include('enterprise.themanager.urls')),
)
