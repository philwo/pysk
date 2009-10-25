#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import shutil
import cPickle
import urllib2
import socket

APIPASS = "W68p20YST5Iv6KGG"
hostname = socket.getfqdn()

authhandler = urllib2.HTTPBasicAuthHandler()
authhandler.add_password(realm="Pysk API", uri="https://%s/" % (hostname,), user="pysk", passwd=APIPASS)

opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

configdata = cPickle.load(urllib2.urlopen("https://%s/api/v0/vz/apache/" % (hostname,)))

if not "nginx" in configdata:
    exit(0)

vhosts = configdata["nginx"]["vhosts"]
ips = configdata["nginx"]["ips"]
validDomain = re.compile("([a-zA-Z0-9-]+\.?)+")

if os.path.exists("/etc/nginx/conf/sites-available/"):
	shutil.rmtree("/etc/nginx/conf/sites-available/")
if os.path.exists("/etc/nginx/conf/sites-enabled/"):
	shutil.rmtree("/etc/nginx/conf/sites-enabled/")
os.mkdir("/etc/nginx/conf/sites-available/", 0755)
os.mkdir("/etc/nginx/conf/sites-enabled/", 0755)

for vhosttuple in vhosts:
    key = vhosttuple[0]
    value = vhosttuple[1]

    if validDomain.match(key).group(0) != key:
        raise Exception("Invalid domain name = '%s'!" % (key,))

    print "Generating virtual host '%s' ..." % (key,)
    outpath = "/etc/nginx/conf/sites-available/%s" % (key,)
    f = open(outpath, "w")
    f.writelines(value)
    f.close()

    subprocess.call(["ln", "-s", "/etc/nginx/conf/sites-available/" + key, "/etc/nginx/conf/sites-enabled/" + key])

