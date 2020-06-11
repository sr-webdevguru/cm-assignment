from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views
from django.views.decorators.csrf import csrf_exempt

from apps.authentication.health_check import healthcheck
from apps.authentication.views import entry_point
from apps.authentication.views import password_reset_final
from apps.authentication.views import password_reset_token_check
from apps.authentication.views import version_entry_point
from apps.data_sync.views import upload_language_file
from apps.incidents.views import media_access
from apps.mkdocs.urls import doc_url
from apps.router import auth_urls
from apps.router import router

urlpatterns = patterns('',
                       url(r'^api/$', entry_point),
                       url(r'^api/v3/$', version_entry_point),
                       url(r'^api/v3/', include(auth_urls + router.urls)),
                       url(r'^api/v3/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="my_login"),
                       url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
                       url(r'^admin/addlanguage/$', upload_language_file, name="file upload"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^docs/', include(doc_url)),
                       url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           csrf_exempt(password_reset_final), name='password_reset_confirm'),
                       url(r'^tokencheck/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           csrf_exempt(password_reset_token_check), name='password_reset_token_check'),
                       url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
                       url(r'^check/$', healthcheck),
                       url(r'^health/$', include('health_check.urls')),
                       url(r'^content/(?P<resort_id>[^/]+)/(?P<incident_id>[^/]+)/', media_access)
                       )


# if settings.DEBUG:
# import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )
