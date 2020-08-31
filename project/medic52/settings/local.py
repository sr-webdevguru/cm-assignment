from medic52.settings.common import *

__author__ = 'jimit'

# Database setting for local environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

INSTALLED_APPS = COMMON_APPS

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

TEMPLATE_DIRS += (os.path.join(STATIC_ROOT, 'content'),)

MEDIA_ROOT = '/code/project'

STATICFILES_DIRS = (("project", os.path.join(BASE_DIR, 'medic52/static-content')),)

DEFAULT_FROM_EMAIL = 'xyz@gmail.com'

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = "xyz@gmail.com"

EMAIL_HOST_PASSWORD = "xyz123"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEBUG = True

WSGI_APPLICATION = "wsgi.application"

SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_ROOT = os.path.join(BASE_DIR, 'media')
SENDFILE_URL = '/media'

RUN_ENV = "local"

# AWS Settings
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
GLOBAL_KMS_KEY_ID = os.environ['GLOBAL_KMS_KEY_ID']
AWS_REGION = os.environ['AWS_REGION']
BUCKET_NAME = os.environ['S3_BUCKET_NAME']

