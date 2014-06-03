from django.conf.urls import patterns, url
from steam_user import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^list_all/$', views.list_all_user, name='list_all_user'),
    url(r'^search$', views.search.as_view(), name='search'),
    url(r'^(?P<user_id>\d+)/$', views.user_profile, name='user_profile'),
    # url(r'^user_profile/$', views.SteamUserView.as_view(), name='steam_user_profile'),
    # url(r'^user_profile_new/$', views.steam_user_profile_new, name='steam_user_profile_new'),
)

