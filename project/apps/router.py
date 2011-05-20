from django.conf.urls import patterns, url
from django.contrib.auth import views
from rest_framework.routers import DefaultRouter

from apps.asset.views import AssetViewSet, AssetTypeViewSet
from apps.authentication.views import Impersonate
from apps.authentication.views import Login
from apps.authentication.views import Logout
from apps.authentication.views import OauthApp
from apps.authentication.views import password_reset
from apps.controlled_substance.views import AuditLogViewSet
from apps.controlled_substance.views import ControlledSubstancesViewSet
from apps.custom_user.views import Register
from apps.custom_user.views import RolesUser
from apps.custom_user.views import UserViewSet
from apps.data_sync.views import DataSync
from apps.data_sync.views import GetLanguageFile
from apps.data_sync.views import receive_upload
from apps.devices.views import DeviceViewSet
from apps.devices.views import heartbeat
from apps.incidents.analytics import activity
from apps.incidents.analytics import age
from apps.incidents.analytics import alcohol
from apps.incidents.analytics import gender
from apps.incidents.analytics import injury_types
from apps.incidents.analytics import patrollers
from apps.incidents.analytics import referred_to
from apps.incidents.views import Config, upload_file_to_s3
from apps.incidents.views import IncidentNotesView
from apps.incidents.views import IncidentStatusView
from apps.incidents.views import IncidentViewSet
from apps.incidents.views import get_status_list
from apps.incidents.views import public_incident
from apps.reports.views import ReportViewset, StatusIncidentAPIView
from apps.resorts.views import AreaViewSet
from apps.resorts.views import LocationViewSet
from apps.resorts.views import ResortViewSet
from apps.routing.views import discover

router = DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'resorts', ResortViewSet, 'resorts')
router.register(r'devices', DeviceViewSet, 'devices')
router.register(r'incidents', IncidentViewSet, 'incidents')
router.register(r'reports', ReportViewset, 'reports')
router.register(r'areas', AreaViewSet, 'areas')
router.register(r'locations', LocationViewSet, 'locations')
router.register(r'assets/types', AssetTypeViewSet, 'assets-types')
router.register(r'assets', AssetViewSet, 'assets')
router.register(r'controlled_substances/auditlog', AuditLogViewSet, 'auditlog')
router.register(r'controlled_substances', ControlledSubstancesViewSet, 'controlled_substances')

auth_urls = patterns('',
                     url(r'^auth/discover/', discover),
                     url(r'^auth/login/', Login.as_view()),
                     url(r'^auth/logout/', Logout.as_view()),
                     url(r'^auth/register/', Register.as_view()),
                     url(r'^users/roles', RolesUser.as_view()),
                     url(r'^auth/password_reset/$', password_reset, name='password_reset'),
                     url(r'^auth/password_reset/done/$', views.password_reset_done, name='password_reset_done'),

                     # Impersonate mode
                     url(r'^auth/impersonate/(?P<user_id>[^/]+)/', Impersonate.as_view()),

                     # oAuth generation for resort
                     url(r'^resort_oauth/$', OauthApp.as_view(), name='password_reset_done'),

                     # Heartbeat API URL
                     url(r'^devices/(?P<device_id>[^/]+)/heartbeat/$', heartbeat),

                     # Incident related URL
                     url(r'^incidents/config/', Config.as_view()),
                     url(r'^incidents/status/$', get_status_list),
                     url(r'^incidents/(?P<uuid>[^/]+)/status/$', IncidentStatusView.as_view()),
                     url(r'^incidents/(?P<uuid>[^/]+)/notes/$', IncidentNotesView.as_view()),

                     # For public incidents
                     url(r'^incidents/public/', public_incident),
                     url(r'^s3/', upload_file_to_s3),
                     # Data sync URL
                     url(r'sync/$', DataSync.as_view()),

                     # Upload URL
                     url(r'upload/lang/$', receive_upload),

                     # Language file
                     url(r'language/$', GetLanguageFile.as_view()),

                     # Analytics URL
                     url(r'analytics/gender', gender),
                     url(r'analytics/activity', activity),
                     url(r'analytics/injury_types', injury_types),
                     url(r'analytics/referred_to', referred_to),
                     url(r'analytics/age', age),
                     url(r'analytics/alcohol', alcohol),
                     url(r'analytics/patrollers', patrollers),

                     # Report URL
                     url(r'reports/status/', StatusIncidentAPIView.as_view())
                     )
