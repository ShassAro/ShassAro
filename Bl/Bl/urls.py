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

image_list = views.ImageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
image_detail = views.ImageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

learning_path_list = views.LearningPathViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
learning_path_detail = views.LearningPathViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

game_user_list = views.GameUserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
game_user_detail = views.GameUserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

shassaro_list = views.ShassaroViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
shassaro_detail = views.ShassaroViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

game_list = views.GameViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
game_detail = views.GameViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

game_result_list = views.GameResultViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
game_result_detail = views.GameResultViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

badge_list = views.BadgeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
badge_detail = views.BadgeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

docker_server_list = views.DockerServerViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
docker_server_detail = views.DockerServerViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

configurations_list = views.ConfigurationsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
configurations_detail = views.ConfigurationsViewSet.as_view({
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

    url(r'^images/$', image_list),
    url(r'^images/(?P<pk>[a-zA-z]+)/$', image_detail),

    url(r'^learning_paths/$', learning_path_list),
    url(r'^learning_paths/(?P<pk>[a-zA-z]+)/$', learning_path_detail),

    url(r'^game_users/$', game_user_list),
    url(r'^game_users/(?P<pk>[a-zA-z]+)/$', game_user_detail),

    url(r'^shassaros/$', shassaro_list),
    url(r'^shassaros/(?P<pk>[a-zA-z]+)/$', shassaro_detail),

    url(r'^games/$', game_list),
    url(r'^games/(?P<pk>[a-zA-z]+)/$', game_detail),

    url(r'^game_results/$', game_result_list),
    url(r'^game_results/(?P<pk>[a-zA-z]+)/$', game_result_detail),

    url(r'^badges/$', badge_list),
    url(r'^badges/(?P<pk>[a-zA-z]+)/$', badge_detail),

    url(r'^docker_servers/$', docker_server_list),
    url(r'^docker_servers/(?P<pk>[a-zA-z]+)/$', docker_server_detail),

    url(r'^configurations/$', configurations_list),
    url(r'^configurations/(?P<pk>[a-zA-z]+)/$', configurations_detail),
)

urlpatterns = format_suffix_patterns(urlpatterns)