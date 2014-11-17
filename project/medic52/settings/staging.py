from medic52.settings.common import *

# Database setting for local environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

INSTALLED_APPS = COMMON_APPS + ('raven.contrib.django.raven_compat',)

STATIC_URL = '/static/'

STATIC_ROOT = '/data/www/api.staging.medic52.com/static'

TEMPLATE_DIRS += (os.path.join(STATIC_ROOT, 'content'),)

STATICFILES_DIRS = (("project", os.path.join(BASE_DIR, 'medic52/static-content')),)

MEDIA_ROOT = '/data/www/api.staging.medic52.com'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'LITq2mC3pv3c')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'duncan@medic52.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
# EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
# SERVER_EMAIL = EMAIL_HOST_USER

# Configuration for sentry
RAVEN_CONFIG = {
    'dsn': 'http://023cc7721c944754a574a3b6f55d5350:2e6679b9025146c2a4427a1a6df41e49@sentry.medic52.com/3',
    'site': 'Medic52 Staging'
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

DEBUG = True

WSGI_APPLICATION = "wsgi.application"

SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_ROOT = os.path.join(MEDIA_ROOT, 'media')
SENDFILE_URL = '/media'

SESSION_COOKIE_SECURE = True

RUN_ENV = "staging"

os.environ['HTTPS'] = "on"

TEMPLATE_DIRS += (os.path.join(STATIC_ROOT, 'content'),)

# AWS Settings
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
GLOBAL_KMS_KEY_ID = os.environ['GLOBAL_KMS_KEY_ID']
AWS_REGION = os.environ['AWS_REGION']
BUCKET_NAME = os.environ['S3_BUCKET_NAME']

