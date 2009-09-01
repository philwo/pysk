#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import urllib2

APIPASS = open("/etc/pysk/apipass", "r").read().strip()

authhandler = urllib2.HTTPDigestAuthHandler()
authhandler.add_password("private area", "pysk.igowo.de", "pysk", APIPASS)

opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

zonefiles = cPickle.load(urllib2.urlopen("https://pysk.igowo.de/api/v0/dns/bind/"))
conf = []

for key, value in zonefiles.iteritems():
	print "Generating zone '%s' ..." % (key,)
	outpath = "/var/named/pysk/db.%s" % (key,)
	f = open(outpath, "w")
	f.writelines(value)
	conf.append('zone "%s" { type master; file "%s"; allow-query { any; }; };' % (key, outpath))
	f.close()

f = open("/var/named/zones.pysk", "w")
f.writelines("\n".join(conf))
f.close()
