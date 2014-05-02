from django.conf.urls import patterns, url
from steam import views


urlpatterns = patterns('',
#  ex: /polls/
#    url(r'^$', views.index, name='index'),
#    # ex: /polls/5/
#    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
#    # ex: /polls/5/results/
#    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
#    # ex: /polls/5/vote/
#    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),

	url(r'^$', views.index, name='index'),

    url(r'^login/$', 'django.contrib.auth.views.login',
            {'template_name': 'steam/login.html'},name='loginPage'),

    url(r'^userLogin/$', views.user_login, name='user_login'),

    url(r'^userLogout/$', views.user_logout, name='user_logout'),


	# url(r'^contact/$', views.ContactView.as_view(), name='contact'),
	# url(r'^contact/thanks/$', views.ThanksView.as_view(), name='thanks'),
	# url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	# url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
	# url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)

