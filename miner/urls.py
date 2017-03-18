from django.conf.urls import url
from miner import views

urlpatterns = [
    url(r'^create/$', views.create_game, name='create_game'),
]
