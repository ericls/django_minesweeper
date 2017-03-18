from django.conf.urls import url, include
from miner import api, views

api_urlpatterns = [
    url(r'^create/$', api.create_game, name='create_game'),
    url(r'^game/(?P<pk>\d+)/action/$', api.apply_action, name='apply_action'),
    url(r'^game/(?P<pk>\d+)/back/$', api.go_back, name='go_back'),
    url(r'^game/(?P<pk>\d+)$', api.get_game, name='get_game'),
]

urlpatterns = [
    url(r'^api/', include(api_urlpatterns)),
    url(r'^$', views.index, name='index'),
]
