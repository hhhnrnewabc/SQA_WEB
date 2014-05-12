from django.conf.urls import patterns, url, include
from steam_dev import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^dev_profile$', views.SteamDevView.as_view(), name='dev_profile'),
    url(r'^dev_apply$', views.SteamDevApplyView.as_view(), name='dev_apply'),


    url(r'^api/steam_user_list$', views.SteamUserList.as_view(), name="steam_user_list"),
    url(r'^api/steam_dev_list$', views.SteamDeveloperList.as_view(), name="steam_dev_list"),

)

urlpatterns += format_suffix_patterns(patterns('steam_dev.views',
                                               url(r'^api$', 'api_root',name="api_root" ),
))