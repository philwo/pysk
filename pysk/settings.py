# -*- coding: utf-8 -*-

# Django settings for pysk project.

import sys
import os
import os.path
import socket

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
MY_IP = socket.gethostbyaddr(socket.gethostname())[2][0]
MY_HOSTNAME = socket.gethostbyaddr(socket.gethostname())[0]

DEBUG = False
TEMPLATE_DEBUG = DEBUG

if TEMPLATE_DEBUG == True:
	TEMPLATE_STRING_IF_INVALID = "TEMPLATE_INVALID"

ADMINS = (
	("Philipp Wollermann", "philipp@igowo.de"),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = "pysk@%s" % (MY_HOSTNAME,)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

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

USE_I18N = True

# MEDIA_* settings are only relevant for uploaded files,
# specifically fields of type FileField and ImageField!
MEDIA_ROOT = os.path.join(PROJECT_PATH, '../uploads')
MEDIA_URL = '/uploads/'
STATIC_ROOT = os.path.join(PROJECT_PATH, '../static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

SECRET_KEY = 'xgYRsDMhGsnjubsP1JwT9b6ux6teGVLedHEJywNtIsMQKxgK'

SEND_BROKEN_LINK_EMAILS = not DEBUG
APPEND_SLASH = False
PREPEND_WWW = False
USE_ETAGS = True

ROOT_URLCONF = 'pysk.urls'

AUTH_PROFILE_MODULE = "app.customer"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/admin/"
ACCOUNT_ACTIVATION_DAYS = 14


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.request",
)

TEMPLATE_DIRS = (
	"/opt/pysk/pysk/templates",
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.admin',
	'django.contrib.webdesign',
	'django_extensions',
	'pysk.app',
	'pysk.vps',
)

