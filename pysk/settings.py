# -*- coding: utf-8 -*-

# Django settings for pysk project.

from os import path as os_path
PROJECT_PATH = os_path.abspath(os_path.split(__file__)[0])

DEBUG = False
TEMPLATE_DEBUG = DEBUG

if TEMPLATE_DEBUG == True:
	TEMPLATE_STRING_IF_INVALID = "TEMPLATE_INVALID"

ADMINS = (
	("Philipp Wollermann", "philipp@igowo.de"),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'pysk'                  # Or path to database file if using sqlite3.
DATABASE_USER = 'pysk'                  # Not used with sqlite3.
DATABASE_PASSWORD = 'z62VUW2m59Y69u99'
DATABASE_HOST = ''                      # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                      # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de-de'

_ = lambda s: s

LANGUAGES = (
	('de', _('German')),
	('en', _('English')),
)

SITE_ID = 1
USE_I18N = True

# MEDIA_* settings are only relevant for uploaded files,
# specifically fields of type FileField and ImageField!
MEDIA_ROOT = os_path.join(PROJECT_PATH, '../uploads')
MEDIA_URL = '/uploads/'
STATIC_ROOT = os_path.join(PROJECT_PATH, '../static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

SECRET_KEY = 'xgYRsDMhGsnjubsP1JwT9b6ux6teGVLedHEJywNtIsMQKxgK'

ROOT_URLCONF = 'pysk.urls'
AUTH_PROFILE_MODULE = "app.customer"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/admin/"
ACCOUNT_ACTIVATION_DAYS = 14

DEFAULT_FROM_EMAIL = "support@igowo.de"
SEND_BROKEN_LINK_EMAILS = not DEBUG
APPEND_SLASH = False
PREPEND_WWW = False
USE_ETAGS = True

# Hostname and IP of this server
import socket
MY_IP = socket.gethostbyaddr(socket.gethostname())[2][0]
MY_HOSTNAME = socket.gethostbyaddr(socket.gethostname())[0]

TEMPLATE_DIRS = (
	"/opt/pysk/pysk/templates",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
	'django.middleware.gzip.GZipMiddleware',
	'django.middleware.http.ConditionalGetMiddleware',
	'django.contrib.csrf.middleware.CsrfMiddleware',
	'django.middleware.common.CommonMiddleware',
	#'babeldjango.middleware.LocaleMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'pysk.app.middleware.HttpAuthMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
	'django.middleware.http.ConditionalGetMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.webdesign',
	#'babeldjango',
	'django_extensions',
	'pysk.app',
	'pysk.vps',
)
