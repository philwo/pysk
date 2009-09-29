#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import urllib2

APIPASS = "W68p20YST5Iv6KGG"

servers = ["mikuru", "kyon", "yuki",
"c-ds",
"c-ps1-1",
#"c-philwo-1",
#"c-mehlis-1",
#"c-spt-1",
#"c-kpni-1",
#"c-wygand-1",
#"c-eot-1",
#"c-jf-1",
#"c-hermanussen-1",
#"c-ernst-1",
#"c-gfa-1",
#"c-chris-1",
#"c-simon-1",
#"c-kg24-1",
#"c-elsenkoch-1",
#"c-healit-1",
#"c-dw30-1",
#"c-schreiber-1",
]

authhandler = urllib2.HTTPBasicAuthHandler()
for s in servers:
	authhandler.add_password(realm="Pysk API", uri="https://%s:8080/" % (s,), user="pysk", passwd=APIPASS)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

conf = []
for s in servers:
	zonefiles = cPickle.load(urllib2.urlopen("https://%s:8080/api/v0/dns/bind/" % (s,)))
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

