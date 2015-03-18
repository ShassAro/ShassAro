from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import TagViewSet

tag_list = TagViewSet.as_view({
    'get':'list',
    'post':'create'
})

tag_detail = TagViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Bl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^tags/$', tag_list),
    url(r'^tags/(?P<pk>[0-9]+)/$', tag_detail)
)
