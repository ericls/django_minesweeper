from django.conf.urls import url
from miner import views

urlpatterns = [
    url(r'^create/$', views.create_game, name='create_game'),
    url(r'^game/(?P<pk>\d+)/action/$', views.apply_action, name='apply_action'),
    url(r'^game/(?P<pk>\d+)/back/$', views.go_back, name='go_back'),
    url(r'^game/(?P<pk>\d+)$', views.get_game, name='get_game'),
]
