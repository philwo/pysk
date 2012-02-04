#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright 2006 - 2012 Philipp Wollermann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import cPickle
import urllib2
import yaml
import pycurl
from cStringIO import StringIO


class Test:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf

APIPASS = "XXXXXXXXXXX"

servers = [host for host in yaml.load_all(open("/var/named/hosts.yml", "r"))]

authhandler = urllib2.HTTPBasicAuthHandler()
for s in servers:
    authhandler.add_password(realm="Pysk", uri="https://%s.igowo.de/" % (s["name"],), user="pysk", passwd=APIPASS)
    authhandler.add_password(realm="Pysk API", uri="https://%s.igowo.de/" % (s["name"],), user="pysk", passwd=APIPASS)

opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

conf = {}
for s in servers:
    #print "%s ..." % (s,)
    try:
        if s["kind"] == "pysk":
            output = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, 'https://pysk:%s@%s.igowo.de/api/v0/dns/bind/' % (APIPASS, s['name']))
            c.setopt(c.WRITEFUNCTION, output.write)
            c.perform()
            c.close()
            output.seek(0)
            zonefiles = cPickle.load(output)
            #zonefiles = cPickle.load(urllib2.urlopen("https://%s.igowo.de/api/v0/dns/bind/" % (s["name"],)))
        else:
            zonefiles = {}
        for key, value in zonefiles.iteritems():
            parent = key
            while parent.count(".") > 1 and not parent in conf:
                parent = ".".join(parent.split(".")[1:])
            if parent in conf and key != parent:
                # Found parent zone for %s: %s" % (key, parent)
                pass

            outpath = "/var/named/pysk/db.%s" % (parent,)
            if not parent in conf:
                # New zone
                f = open(outpath, "w")
                f.writelines(value)
                conf[parent] = 'zone "%s" { type master; file "%s"; allow-query { any; }; };' % (parent, outpath)
            else:
                # Appending
                f = open(outpath, "a")
                f.write("\n; APPENDING FROM %s\n" % (s["name"],))
                f.write("$ORIGIN %s.\n" % (key,))
                # FIXME quickhack for MX at megowo.de
                if parent == "megowo.de" and key != parent:
                    f.write("@ IN MX 10 %s.igowo.de.\n" % (s["name"],))
                f.write("\n")
                lines = value.split("\n")
                if "; ON APPEND CUT HERE" in lines:
                    while (lines[0] != "; ON APPEND CUT HERE"):
                        del lines[0]
                    del lines[0]
                f.writelines("\n".join(lines))
            f.close()
    except urllib2.URLError as e:
        print >>sys.stderr, "ERROR: Could not get zones from %s !!!" % (s["name"],)
        print >>sys.stderr, e
        pass

# Add servers to igowo.de zone
zonefile = open("/var/named/pysk/db.igowo.de", "a")
zonefile.write("\n; SERVERS\n")
zonefile.write("$ORIGIN igowo.de.\n\n")
zonefile.writelines("\n".join(["%s IN A %s" % (s["name"], s["ip"]) for s in servers]))
zonefile.write("\n")
zonefile.writelines("\n".join(["*.%s IN A %s" % (s["name"], s["ip"]) for s in servers if s["kind"] == "froxlor"]))
zonefile.write("\n")
zonefile.close()

f = open("/var/named/zones.pysk", "w")
f.writelines("\n".join(conf.values()))
f.close()
