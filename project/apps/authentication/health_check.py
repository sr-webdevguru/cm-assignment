from health_check_cache.plugin_health_check import CacheBackend
from health_check_db.plugin_health_check import DjangoDatabaseBackend
from health_check_storage.plugin_health_check import DefaultFileStorageHealthCheck
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

__author__ = 'jimit'


@api_view()
@permission_classes((AllowAny,))
@authentication_classes(())
def healthcheck(request):
    plugin = None

    if request.query_params['type'] == 'db':
        plugin = DjangoDatabaseBackend()
    elif request.query_params['type'] == 'cache':
        plugin = CacheBackend()
    elif request.query_params['type'] == 'storage':
        plugin = DefaultFileStorageHealthCheck()

    if not plugin.status:  # Will return True or None
        return Response({"status": plugin.pretty_status()}, status=500)
    return Response({"status": plugin.pretty_status()}, status=200)
