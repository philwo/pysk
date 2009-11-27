#!/usr/bin/python

import sys, os, os.path

sys.path.insert(0, "/opt/pysk/pysk")
sys.path.insert(0, "/opt/pysk")
os.environ["DJANGO_SETTINGS_MODULE"] = "pysk.settings"

from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string

from pysk.app.models import *
from pysk.vps.models import *

from time import time
from IPy import IP
from pwd import getpwnam

import cPickle
import hashlib
import re
import subprocess
import shutil
import urllib2
import socket

validDomain = re.compile("([a-zA-Z0-9-]+\.?)+")

def mkdir(path, mode):
    print "mkdir    %o  %s" % (mode, path)
    os.mkdir(path, mode)

def symlink(target, source):
    print "symlink  %s  %s" % (target, source)
    os.symlink(target, source)

def rmtree(path):
    print "rmtree   %s" % (path,)
    shutil.rmtree(path)

def makefile(path, content, mode=0644):
    print "makefile %o  %s" % (mode, path,)
    with open(path, "w") as conf:
        conf.write(content)
    os.chmod(path, mode)

# Generate an Apache monit-conf for every user who uses Apache
for customer in set([x.owner for x in VirtualHost.objects.filter(apache_enabled=True)]):
    username = customer.user.username
    apacheroot = "/etc/httpd-%s" % (username,)
    ipoffset = customer.kundennr - 10000
    assert(ipoffset >= 0)
    logpath = "/var/log/httpd-%s/" % (username,)
    runpath = "/var/run/httpd-%s/" % (username,)
    
    uid = getpwnam(username).pw_uid
    gid = getpwnam(username).pw_gid

    if not os.path.exists(logpath):
        mkdir(logpath, 0755)
    if not os.path.exists(runpath):
        mkdir(runpath, 0755)
    if not os.path.exists(runpath + "/fastcgi"):
        mkdir(runpath + "/fastcgi", 0700)
    os.chown(runpath + "/fastcgi", uid, gid)
    
    if os.path.exists(apacheroot):
    	rmtree(apacheroot)
    mkdir(apacheroot, 0755)
    symlink("/usr/lib/httpd/build", apacheroot + "/build")
    symlink("/usr/lib/httpd/modules", apacheroot + "/modules")
    symlink(logpath, apacheroot + "/logs")
    symlink(runpath, apacheroot + "/run")
    mkdir(apacheroot + "/conf/", 0755)
    mkdir(apacheroot + "/conf/sites/", 0755)
    symlink("/etc/httpd/conf/magic", apacheroot + "/conf/magic")
    symlink("/etc/httpd/conf/mime.types", apacheroot + "/conf/mime.types")
    
    makefile(apacheroot + "/conf/httpd.conf", render_to_string("etc/httpd/conf/httpd.conf", {"username": username, "ipoffset": ipoffset}))
    makefile(apacheroot + "/conf/sites/000-default", render_to_string("etc/httpd/conf/sites/default", {"ipoffset": ipoffset}))
    makefile("/etc/monit.d/httpd-%s" % (username,), render_to_string("etc/monit.d/httpd", {"username": username, "ipoffset": ipoffset}))

    if not os.path.exists("/srv/http/default/htdocs/"):
    	os.makedirs("/srv/http/default/htdocs/", 0755)
    os.chown("/srv/http/default/htdocs/", 0, 0)
    
    # For every IP of this server, which should be served by an apache
    for vh in VirtualHost.objects.filter(active=True, owner=customer, apache_enabled=True):
        htdocs_dir = "/home/%s/www/%s/htdocs/" % (username, vh.fqdn())

        extra_aliases = ""
        for da in DirectAlias.objects.filter(active=True).filter(host=vh):
            extra_aliases += " %s" % (da.fqdn(),)
        
        apache_config = "\n".join(["    "+x for x in vh.apache_config.replace("\r\n", "\n").split("\n")])

        output = []
        ports = ("80",) if not vh.ssl_enabled else ("80", "81")
        for port in ports:
            output.append(render_to_string("etc/httpd/conf/sites/site", {
                "ipoffset": ipoffset,
                "port": port,
                "fqdn": vh.fqdn(),
                "extra_aliases": extra_aliases,
                "htdocsdir": htdocs_dir,
                "apache_config": apache_config,
                "enable_php": vh.enable_php,
            }))
        makefile(apacheroot + "/conf/sites/%s" % (vh.fqdn(),), "\n".join(output))
    
        # Fixup htdocs dir
        gid = 100

        for dir in [os.path.realpath(htdocs_dir), os.path.realpath(os.path.join(htdocs_dir, "../"))]:
            if not os.path.exists(dir):
                print "WARNING: htdocs dir does not exist: %s" % (dir)
                os.makedirs(dir, 0755)

            statinfo = os.stat(dir)
            if not statinfo.st_uid == uid:
                print "WARNING: htdocs dir has wrong owner: %i != %i" % (uid, statinfo.st_uid)
                os.chown(dir, uid, -1)
            if not statinfo.st_gid == gid:
                print "WARNING: htdocs dir has wrong group: %i != %i" % (gid, statinfo.st_gid)
                os.chown(dir, -1, gid)

    makefile("/usr/sbin/apachectl-%s" % (username,), render_to_string("usr/bin/apachectl", {"username": username, "ipoffset": ipoffset}), 0755)
    subprocess.call(["/usr/sbin/apachectl-%s" % (username,), "restart"])

# Generate a PHP monit-conf for every user who uses PHP
for customer in set([x.owner for x in VirtualHost.objects.filter(enable_php=True)]):
    username = customer.user.username
    makefile("/etc/php/php-%s.sh" % (username,), render_to_string("etc/php/php.sh", {"username": username, "php_instances": 5}), 0755)
    makefile("/etc/monit.d/php-%s" % (username,), render_to_string("etc/monit.d/php", {"username": username}))

makefile("/etc/php/php-pysk.sh", render_to_string("etc/php/php.sh", {"username": "pysk", "php_instances": 1}), 0755)
makefile("/etc/monit.d/php-pysk", render_to_string("etc/monit.d/php", {"username": "pysk"}))

subprocess.call(["/usr/bin/monit", "reload"])
