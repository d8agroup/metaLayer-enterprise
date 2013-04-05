from django.conf.urls.defaults import patterns, url
from singleuserenv import views

urlpatterns = patterns(
    '',
    url(r'', views.home),
)

