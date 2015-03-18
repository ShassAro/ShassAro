from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
import views


tag_list = views.TagViewSet.as_view({
    'get':'list',
    'post':'create'
})
tag_detail = views.TagViewSet.as_view({
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
    url(r'^tags/(?P<pk>[a-zA-z]+)/$', tag_detail),
)

urlpatterns = format_suffix_patterns(urlpatterns)