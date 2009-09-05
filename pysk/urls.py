# -*- coding: utf-8 -*-

import re
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from pysk.vps.models import *

admin.autodiscover()

ip4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')

def navigation(request):
	dict = {}
	url = request.path
	urlparts = url.strip("/").split("/")

	navisection = None

	if urlparts[0] == "vps":
		if len(urlparts) > 1:
			if urlparts[1] == "management":
				navisection = "management"

	dict["navisection"] = navisection

	return dict

urlpatterns = patterns("",
	(r'^admin/(.*)', admin.site.root),
)

"""
urlpatterns = patterns("pysk.vps1.views",
	(r"^vps/$", "overview"),

	# accounts
	(r"^accounts/", include("pysk.registration.urls")),

	# management
	(r"^vps/management/$", "management"),
	(r"^vps/management/convert/$", "convert"),

	(r"^vps/management/users/$", "user_list"),
	(r"^vps/management/users/add/$", "user_create"),
	(r"^vps/management/users/(?P<object_id>\d+)/$", "user_detail"),
	(r"^vps/management/users/(?P<object_id>\d+)/edit/$", "user_edit"),
	(r"^vps/management/users/(?P<object_id>\d+)/delete/$", "user_delete"),

	(r"^vps/management/domains/$", "domain_list"),
	(r"^vps/management/domains/add/$", "domain_create"),
	(r"^vps/management/domains/(?P<object_id>\d+)/$", "domain_detail"),
	(r"^vps/management/domains/(?P<object_id>\d+)/edit/$", "domain_edit"),
	(r"^vps/management/domains/(?P<object_id>\d+)/delete/$", "domain_delete"),

	(r"^vps/management/nsentries/$", "nsentry_list"),
	(r"^vps/management/nsentries/add/$", "nsentry_create"),
	(r"^vps/management/nsentries/(?P<object_id>\d+)/$", "nsentry_detail"),
	(r"^vps/management/nsentries/(?P<object_id>\d+)/edit/$", "nsentry_edit"),
	(r"^vps/management/nsentries/(?P<object_id>\d+)/delete/$", "nsentry_delete"),

	(r"^vps/management/ip/$", "ipaddress_list"),
	(r"^vps/management/ip/add/$", "ipaddress_create"),
	(r"^vps/management/ip/(?P<object_id>\d+)/$", "ipaddress_detail"),
	(r"^vps/management/ip/(?P<object_id>\d+)/edit/$", "ipaddress_edit"),
	(r"^vps/management/ip/(?P<object_id>\d+)/delete/$", "ipaddress_delete"),

	# resources

	# upgrades

	# help

#	(r"^vps/view/nsentries/$", "view_nsentries"),
#	(r"^vps/view/ips/$", "view_ips"),
#	(r"^vps/view/vhosts/$", "view_vhosts"),
#	(r"^vps/view/webapps/$", "view_webapps"),
#	(r"^vps/view/mountpoints/$", "view_mountpoints"),
#	(r"^vps/view/mailboxes/$", "view_mailboxes"),
#	(r"^vps/view/forwardings/$", "view_forwardings"),

#	(r"^vps/add/domain/$", "add_domain"),
#	(r"^vps/add/nsentry/$", "add_nsentry"),
#	(r"^vps/add/ip/$", "add_ip"),
#	(r"^vps/add/vhost/$", "add_vhost"),
#	(r"^vps/add/webapp/php/$", "add_webapp_php"),
#	(r"^vps/add/webapp/django/$", "add_webapp_django"),
#	(r"^vps/add/webapp/redirect/$", "add_webapp_redirect"),
#	(r"^vps/add/mountpoint/$", "add_mountpoint"),
#	(r"^vps/add/mailbox/$", "add_mailbox"),
#	(r"^vps/add/forwarding/$", "add_forwarding"),

#	(r"^vps/edit/domain/(?P<pk>[\w\d\.]*)/$", "edit_domain"),
#	(r"^vps/edit/nsentry/(?P<pk>[\d\.]*)/$", "edit_nsentry"),
#	(r"^vps/edit/ip/(?P<pk>[\d\.]*)/$", "edit_ip"),
#	(r"^vps/edit/vhost/(?P<pk>[\d\.]*)/$", "edit_vhost"),
#	(r"^vps/edit/webapp/(?P<pk>[\d\.]*)/$", "edit_webapp"),
#	(r"^vps/edit/webapp/php/(?P<pk>[\d\.]*)/$", "edit_webapp_php"),
#	(r"^vps/edit/webapp/django/(?P<pk>[\d\.]*)/$", "edit_webapp_django"),
#	(r"^vps/edit/webapp/redirect/(?P<pk>[\d\.]*)/$", "edit_webapp_redirect"),
#	(r"^vps/edit/mountpoint/(?P<pk>[\d\.]*)/$", "edit_mountpoint"),
#	(r"^vps/edit/mailbox/(?P<pk>[\d\.]*)/$", "edit_mailbox"),
#	(r"^vps/edit/forwarding/(?P<pk>[\d\.]*)/$", "edit_forwarding"),
)
"""

# Muss per HTTP Digest abgesichert werden!
urlpatterns += patterns("pysk.vps.views",
	(r'^api/v0/vz/(?P<server>.*)/apache/', 'v0_apache'),
	(r'^api/v0/vz/(?P<server>.*)/aliases/', 'v0_aliases'),
	(r'^api/v0/vz/(?P<server>.*)/aliases_nginx/', 'v0_aliases_nginx'),
	(r'^api/v0/dns/bind/', 'bind'),
	#(r'^migrate/', 'migrate'),
)

urlpatterns += patterns("pysk.main.views",
	(r'^api/v0/cdr/', 'import_cdr'),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': '/opt/pysk/code/htdocs/'}),
	)
	urlpatterns += patterns('',
		(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': '/opt/pysk/data/uploads/'}),
	)

urlpatterns += patterns("pysk.vps.views",
	(r'^helloworld.pdf$', 'helloworld'),
)

