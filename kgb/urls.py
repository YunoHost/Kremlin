from django.conf.urls import patterns, url


urlpatterns = patterns('kgb.views',
    url(r'^(?P<domain>[^/]+)/(?P<password>[^/]+)/$', 'install_docker', name=''),
)
