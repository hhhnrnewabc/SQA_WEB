from django.conf.urls import patterns, include, url
from django.conf import settings
from SQA_Project import views
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SQA_Project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n'), name='set_language'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^steam/', include('steam.urls', namespace="steam")),
    url(r'^steam/dev/', include('steam_dev.urls', namespace="steam_dev")),
    url(r'^steam/user/', include('steam_user.urls', namespace="steam_user")),

    # if nignx setting location /media/ : won't need it
    # for Filename and path attacks : use under line
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
# urlpatterns += patterns('',
#     url(r'^i18n/', include('django.conf.urls.i18n'), name='set_language'),
#     # url(r'^$', TemplateView.as_view(template_name='select_language.html'), name='select_language'),
# )

handler404 = views.steam_404_view

