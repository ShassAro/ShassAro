from django.conf.urls import patterns, include, url
from django.contrib import admin
from DockerRestView import DockerDeployRestView, DockerKillRestView, DockerListRestView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DockerAdmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^deploy/(?P<resource_id>\d+)[/]?$', DockerDeployRestView.as_view(), name='docker_rest_view'),
    url(r'^deploy[/]?$', DockerDeployRestView.as_view(), name='docker_rest_view'),
    url(r'^kill/(?P<resource_id>\d+)[/]?$', DockerKillRestView.as_view(), name='docker_rest_view'),
    url(r'^kill[/]?$', DockerKillRestView.as_view(), name='docker_rest_view'),
    url(r'^list[/]?$', DockerListRestView.as_view(), name='docker_rest_view'),
)
