import os, sys
sys.path.append('/opt/pysk/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pysk.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

