from django.conf.urls import patterns, url, include
from game_info import views

urlpatterns = patterns('',
    url(r'^update/$', views.SteamDevAPPSGameInfo.as_view(), name="update")
)
