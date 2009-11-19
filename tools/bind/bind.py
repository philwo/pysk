#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import urllib2
import yaml

APIPASS = "W68p20YST5Iv6KGG"

servers = [host for host in yaml.load_all(open("/opt/pysk/etc/hosts.yml", "r"))]

authhandler = urllib2.HTTPBasicAuthHandler()
for s in servers:
    authhandler.add_password(realm="Pysk", uri="https://%s.igowo.de/" % (s["name"],), user="pysk", passwd=APIPASS)
    authhandler.add_password(realm="Pysk API", uri="https://%s.igowo.de/" % (s["name"],), user="pysk", passwd=APIPASS)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

conf = {}
for s in servers:
    print "Fetching zones from %s ..." % (s["name"],)
    zonefiles = cPickle.load(urllib2.urlopen("https://%s.igowo.de/api/v0/dns/bind/" % (s["name"],)))
    for key, value in zonefiles.iteritems():
        print "-> Generating zone '%s' ... " % (key,),

        parent = key
        while parent.count(".") > 1 and not parent in conf:
            parent = ".".join(parent.split(".")[1:])
        if parent in conf and key != parent:
            print "-> Found parent zone for %s: %s" % (key, parent)

        outpath = "/var/named/pysk/db.%s" % (parent,)
        if not parent in conf:
            print "new"
            f = open(outpath, "w")
            f.writelines(value)
            conf[parent] = 'zone "%s" { type master; file "%s"; allow-query { any; }; };' % (parent, outpath)
        else:
            print "appending"
            f = open(outpath, "a")
            f.write("\n; APPENDING FROM %s\n" % (s["name"],))
            f.write("$ORIGIN %s.\n\n" % (key,))
            lines = value.split("\n")
            if "; ON APPEND CUT HERE" in lines:
                while (lines[0] != "; ON APPEND CUT HERE"):
                    del lines[0]
                del lines[0]
            f.writelines("\n".join(lines))
        f.close()

# Add servers to igowo.de zone
zonefile = open("/var/named/pysk/db.igowo.de", "a")
zonefile.write("\n; SERVERS\n")
zonefile.write("$ORIGIN igowo.de.\n\n")
zonefile.writelines("\n".join(["%s IN A %s" % (s["name"], s["ip"]) for s in servers]))
zonefile.write("\n")
zonefile.close()

f = open("/var/named/zones.pysk", "w")
f.writelines("\n".join(conf.values()))
f.close()

