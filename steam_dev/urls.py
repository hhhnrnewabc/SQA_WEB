from django.conf.urls import patterns, url
from steam_dev import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^dev_profile$', views.SteamDevView.as_view(), name='dev_profile'),
    url(r'^dev_apply$', views.SteamDevApplyView.as_view(), name='dev_apply')
)

