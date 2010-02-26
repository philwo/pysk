# -*- coding: utf-8 -*-

import re
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from os import path as os_path

admin.autodiscover()

ip4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')

def redirect(url):
    def inner(request):
        return HttpResponseRedirect(url)
    return inner

urlpatterns = patterns("",
	(r'^admin/', include(admin.site.urls)),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

# Muss per HTTP Auth abgesichert werden!
urlpatterns += patterns("pysk.vps.views",
	(r'^api/v0/vz/nginx/$', 'v0_nginx'),
	(r'^api/v0/dns/bind/$', 'bind'),
)

urlpatterns += patterns("pysk.vps.views",
    (r'^actions/save/$', 'save'),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^dashboard/$', 'direct_to_template', {'template': 'admin.html'}),
    (r'^navigation/$', 'direct_to_template', {'template': 'navigation.html'}),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
	)
	urlpatterns += patterns('',
		(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)
