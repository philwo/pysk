# -*- coding: utf-8 -*-

# Django settings for pysk project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEFAULT_FROM_EMAIL = "support@igowo.de"
SEND_BROKEN_LINK_EMAILS = True

ADMINS = (
	("Philipp Wollermann", "philipp@igowo.de"),
)

MANAGERS = ADMINS

# New postgres database
DATABASE_ENGINE = 'postgresql_psycopg2' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'pysk'                  # Or path to database file if using sqlite3.
DATABASE_USER = 'pysk'                  # Not used with sqlite3.
DATABASE_PASSWORD = open("/etc/pysk/dbpass", "r").read()
DATABASE_HOST = 'db1.igowo.de'          # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                      # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de-de'

SITE_ID = 1
USE_I18N = True

# MEDIA_* settings are only relevant for uploaded files,
# specifically fields of type FileField and ImageField!
MEDIA_ROOT = '/opt/pysk/data/uploads/'
MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'xgYRsDMhGsnjubsP1JwT9b6ux6teGVLedHEJywNtIsMQKxgK'

ROOT_URLCONF = 'pysk.urls'
AUTH_PROFILE_MODULE = "main.customer"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/vps/"
ACCOUNT_ACTIVATION_DAYS = 14

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"pysk.urls.navigation"
)

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.gzip.GZipMiddleware',
	'django.middleware.http.ConditionalGetMiddleware',
	'django.contrib.csrf.middleware.CsrfMiddleware',
	'django.middleware.common.CommonMiddleware',
	'babeldjango.middleware.LocaleMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)

TEMPLATE_DIRS = (
	"/opt/pysk/templates",
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.webdesign',
	'babeldjango',
	'django_extensions',
	'pysk.main',
	'pysk.vps0',
)

