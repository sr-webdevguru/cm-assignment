"""
Django settings for medic52 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
APPS_DIR = os.path.join(BASE_DIR, 'apps')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '21f2e34h8er9#-1u$v9io#_&$lq*-ie&+w*(g5@87+1to77grf'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

COMMON_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'apps.custom_user',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'apps.resorts',
    'apps.authentication',
    'apps.devices',
    'apps.incidents',
    'apps.reports',
    'apps.routing',
    'apps.data_sync',
    'apps.controlled_substance',
    'apps.asset',
    'rest_framework_swagger',
    'health_check',
    'health_check_db',
    'health_check_cache',
    'health_check_storage',
    'oauth2_provider',
    'corsheaders',
    'sendfile',
    'django_cron',
    'storages',
    'mathfilters'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CRON_CLASSES = [
    "apps.authentication.models.AccessTokenRemove",
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'medic52.urls'

WSGI_APPLICATION = 'medic52.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'medic52/templates'),
    os.path.join(BASE_DIR, 'medic52/templates/api-docs'),
)

# Expires access token after interval of 30 minute
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 1800,
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'apps.authentication.custom_permission_drf.ResortPermission',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.authentication.custom_authentication_drf.OauthAuthentication',
        'apps.authentication.custom_authentication_drf.TokenAuthentication',
        'apps.authentication.custom_authentication_drf.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'helper_functions.CustomPagination',
    'PAGE_SIZE': 100,
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S'
}

AUTH_USER_MODEL = 'custom_user.Users'

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '5wPcFpKEf0FpPszKfCdRms7sE89nue',
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': None,
    'doc_expansion': 'none',
    'token_type': 'Bearer'
}

ENCRYPTED_FIELDS_KEYDIR = os.path.join(BASE_DIR, 'keys')

SESSION_COOKIE_AGE = 7200

# Allow CORS request from all domain
CORS_ORIGIN_ALLOW_ALL = True

# Allowes headers in request
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'token',
)

GPG_PRIVATE_KEY = """-----BEGIN PGP PRIVATE KEY BLOCK-----
VERSION:GnuPG v1

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
BqaEgrFUJjtq+ C /uTTRBrq6uVcWLOVMzvwX8kLX98wVSYFcp/q76N+PtYpVlokNL
4x5GePvPO1poImtW8+QoJlGSpCxSCGO1+DotT8BSW4A4bFhavdF0vQe23E1dXN1k
0tpOeua9DMyJynFv2Z1YcfAf45kDk0QX2AOj/3A=
=p29y
-----END PGP PRIVATE KEY BLOCK-----"""

GPG_PUBLIC_KEY = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v2

mQENBFUfAXYBCAC8qjdz6A7ke1b9s2X6HtGIUt1esFt7CjKKJBIv4DqiUh3h4VYz
falFuzgmLNR2G05jnwRvRJs9T4pxRIVHT+6EjR65Nq8zqoEoyTJrT+YVCveU0Lrk
C1T4DrFF9YwCPIDAR0qO2hOHaNlpLdbWWRS5wX7xRnMIHnJR8qotRREIOXsCzDey
pQRbX7epnYgZGrtmsNQoJ9a0qCbUCp2dQi/FziWYEx4VDDyBA1D1wnENfgE56xmv
bLGe3QKGV6EGCaJfwbzgQ2+CfL7l0IoN4GL19zJJgY4NhXHKddazpyvQLT/tZtLj
gGInjpWw5yP01lBmk4WfqoJj/6O9DY+fs9l7ABEBAAG0SE1lZGljNTIgRGV2ZWxv
cG1lbnQgKERldmVsb3BtZW50IFBISSBlbmNyeXB0aW9uIGtleSkgPGhlbGxvQG1l
ZGljNTIuY29tPokBOAQTAQIAIgUCVR8BdgIbAwYLCQgHAwIGFQgCCQoLBBYCAwEC
HgECF4AACgkQ3EZQ1fwMxtlTiAf9FrDXs2YJUTaXn7uDFM56PtZVSK142cK5pC+v
s8id4NspfFCvZnC0M0OfbGQxsb08A/XkrGYywcwW3sWw/aAsPIBnYmzuArFv43jk
/CT7HeYNByvoiYsVhubYXm+0kHTAJy2/N5LJvyfTC2Gc6u0LgLQeJxUIt/jcq+mM
msgyAwNpnxuw8O8lVO+luDzQ9wawQX/MFVOCWIPzu3ov4wwFCOu2EL+Q4JucT7W1
CgHO0T0JzlE6WMKLSojC7Ze8Bqs/FRi7o59/s2NvOWIA6F393uEj0IWhMkK7d1mB
qtpHKoj3N+W3XkAVYgh+wjCPyuXCDU2oifafvRPQVOYwAxEG67kBDQRVHwF2AQgA
pDiKHj4y5rqQWnH3IOzhj4UUrynZftRpWnIQsh0i6exUqovOv8YQqx0DK7j5ohoR
Rigek19Rx3wrXCSoeuUbF+PRNz80YKqgrZj7obmup+V5sW48XYEqiFYaLYV54NcA
ppSqYHtPvJBCo9Vq9OmBrgO5HTrXpUG41E6xPE/U6WVuH7ZoK9sfFIL0myEyBZI6
YvucCOt/2UC0mtPom0Pag2UAcSk0BfM/fxoMDzT3peETvZz7IEAlluTTio4NDlmL
L7nQU+G2/FyQdd4qA/8Nt0GCw7U97H0Xr3Mo59PpSelmL58srlnOgI81YKAH4Vzx
Uh/QYi3tsPBg09ajyGOFIwARAQABiQEfBBgBAgAJBQJVHwF2AhsMAAoJENxGUNX8
DMbZR8YIALCykMl+Gje74ABRb2bTwgS6dPXeQfNFLI9gwqd2WLusbCNI5PDu5SkP
g79UHDqX0AjHDeVN58ZswFaGfrAAZeLLKog4IjrQYbgxJDT8jJ4EASnxnvCz2fcz
exHtOqRyEE15vUMbbxjh9W5qMV/rgstZaUwjQg9ElwXjUIbW+KpoD9wFBqaEgrFU
Jjtq+C/uTTRBrq6uVcWLOVMzvwX8kLX98wVSYFcp/q76N+PtYpVlokNL4x5GePvP
O1poImtW8+QoJlGSpCxSCGO1+DotT8BSW4A4bFhavdF0vQe23E1dXN1k0tpOeua9
DMyJynFv2Z1YcfAf45kDk0QX2AOj/3A=
=Ymij
-----END PGP PUBLIC KEY BLOCK-----"""

SCHEME = 'https://'

# For Django storage module
AWS_QUERYSTRING_AUTH = False
