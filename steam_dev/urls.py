from django.conf.urls import patterns, url, include
from steam_dev import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^dev_apply/$', views.SteamDevApplyView.as_view(), name='dev_apply'),
    url(r'^dev_profile/$', views.SteamDevProfileView.as_view(), name='dev_profile'),
    url(r'^dev_profile/update_secret_token/$', views.update_secret_token, name='update_secret_token'),

    url(r'^api/$', views.APIRoot.as_view(), name="api_root"),
    url(r'^api/steam_user_list$', views.SteamUserList.as_view(), name="steam_user_list"),
    url(r'^api/steam_user_check$', views.SteamUserCheck.as_view(), name="steam_user_check"),
    url(r'^api/steam_dev_list$', views.SteamDeveloperList.as_view(), name="steam_dev_list"),

)

# urlpatterns += format_suffix_patterns(patterns('steam_dev.views',
#                                                url(r'^api/$', views.APIRoot.as_view(),name="api_root" ),
# ))
