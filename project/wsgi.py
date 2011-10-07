"""
WSGI config for medic52 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
from django.conf import settings

# if settings.RUN_ENV != 'local':
    # import newrelic.agent

    # newrelic.agent.initialize('newrelic.ini')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
