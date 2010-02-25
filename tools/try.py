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
from grp import getgrnam
from glob import glob

import cPickle
import hashlib
import re
import subprocess
import shutil
import urllib2
import socket
import time
import difflib

validDomain = re.compile("([a-zA-Z0-9-]+\.?)+")

# Utility functions
def symlink(target, source):
    print "symlink       %s  %s" % (target, source)
    os.symlink(target, source)

def rmtree(path):
    print "rmtree        %s" % (path,)
    shutil.rmtree(path)

def remove(path):
    print "remove        %s" % (path,)
    os.remove(path)

def copyfile(fromfile, tofile):
    print "copyfile      %s  %s" % (fromfile, tofile)
    shutil.copy(fromfile, tofile)
    
def rename(fromfile, tofile):
    print "rename        %s  %s" % (fromfile, tofile)
    os.rename(fromfile, tofile)

def runprog(args):
    print "runprog       %s" % (" ".join(args))
    subprocess.call(args)

def chown(path, user, group=None):
    print "chown         %s:%s  %s" % (user, group if group else user, path)
    uid = getpwnam(user).pw_uid
    gid = getpwnam(user).pw_gid
    if group != None:
        gid = getgrnam(group).gr_gid
    os.chown(path, uid, gid)

def mkdir(path, mode):
    print "mkdir    %o  %s" % (mode, path)
    os.mkdir(path, mode)

def makefile(path, content, mode=0644, strip_emptylines=False):
    print "makefile %o  %s" % (mode, path,)
    if strip_emptylines:
        content = "\n".join([l for l in content.split("\n") if l.strip()])
    with open(path, "w") as conf:
        conf.write(content)
    os.chmod(path, mode)

def diff(oldfile, newfile, print_on_diff=True, move_on_diff=False, run_on_diff=None):
    print "diff          %s  %s" % (oldfile, newfile)
    fromfile = oldfile

    # Handle not existing old-file case
    fromdate = time.ctime(0)
    fromlines = ""
    if os.path.exists(fromfile):
        fromdate = time.ctime(os.stat(fromfile).st_mtime)
        fromlines = open(fromfile, 'U').readlines()

    tofile = newfile
    todate = time.ctime(os.stat(tofile).st_mtime)
    tolines = open(tofile, 'U').readlines()

    output = "".join(difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=3))
    
    # Backup old file and move new file over
    if move_on_diff and len(output) > 0:
        copyfile(oldfile, oldfile + ".old")
        rename(newfile, oldfile)
    
    if print_on_diff and len(output) > 0:
        print output
        
    if run_on_diff != None:
        run_on_diff()
    
    return output if len(output) > 0 else None

def sync(ist, soll, start_func=None, stop_func=None):
    #print "sync          %s" % (sorted(ist),)
    #print "              %s" % (sorted(soll),)
    for s in soll:
        if s not in ist:
            # Soll, aber ist nicht
            if start_func != None:
                start_func(s)
        else:
            # Soll und ist auch :)
            pass
    for i in ist:
        if i not in soll:
            # Ist, aber soll nicht
            if stop_func != None:
                stop_func(i)

### Clean-up old stuff
if os.path.exists("/etc/nginx/conf/sites-available"):
    rmtree("/etc/nginx/conf/sites-available")
if os.path.exists("/etc/nginx/conf/sites-enabled"):
    rmtree("/etc/nginx/conf/sites-enabled")

### GLOBALS

fqdn = socket.getfqdn()
ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
hypervisor_ip = "188.40.56.202"

### STARTUP
monit_list = [os.path.basename(x) for x in glob("/opt/pysk/serverconfig/etc/monit.d/*")]
monit_list += [os.path.basename(x) for x in glob("/opt/pysk/serverconfig/etc/monit.d/optional/*")]
monit_restart_list = []

### SERVER CONFIG
runprog(["/opt/pysk/serverconfig/copy.sh"])

makefile("/etc/rc.conf", render_to_string("etc/rc.conf", {"hostname": fqdn, "ip": ip, "hypervisor_ip": hypervisor_ip}))

### DOVECOT
statinfo = os.stat("/home/vmail/")
vmail_uid = statinfo.st_uid
vmail_gid = statinfo.st_gid

if os.path.exists("/etc/dovecot/passwd.new"):
    remove("/etc/dovecot/passwd.new")

output = []
for m in Mailbox.objects.filter(active=True).order_by("mail", "domain__name"):
    user = "%s@%s" % (m.mail, m.domain)
    password = m.password
    quota = "user_quota=maildir:storage=%s" % (m.quota * 1024,)
    home = "/home/vmail/%s/%s/" % (m.domain, m.mail)
    output.append("%s:%s:%s:%s::%s::%s" % (user, password, vmail_uid, vmail_gid, home, quota))

makefile("/etc/dovecot/passwd.new", "\n".join(output) + "\n", 0600)
d = diff("/etc/dovecot/passwd", "/etc/dovecot/passwd.new", move_on_diff=True)

### POSTFIX
# virtual_mailboxes
makefile("/etc/postfix/virtual_mailboxes.new", "\n".join(["%s@%s\t%s/%s/Maildir/" % (m.mail, m.domain, m.domain, m.mail) for m in Mailbox.objects.filter(active=True)]) + "\n")
diff("/etc/postfix/virtual_mailboxes", "/etc/postfix/virtual_mailboxes.new", move_on_diff=True)
runprog(["/usr/sbin/postmap", "/etc/postfix/virtual_mailboxes"])

# virtual_domains
domains = sorted(set([m.domain.name for m in Mailbox.objects.filter(active=True)]) | set([f.domain.name for f in Forwarding.objects.filter(active=True)]))
makefile("/etc/postfix/virtual_domains.new", "\n".join(["%s\tdummy" % (d,) for d in domains]) + "\n")
diff("/etc/postfix/virtual_domains", "/etc/postfix/virtual_domains.new", move_on_diff=True)
runprog(["/usr/sbin/postmap", "/etc/postfix/virtual_domains"])

# virtual_forwardings
POSTMASTER_ADDRESS = "philipp@igowo.de"
ABUSE_ADDRESS = "philipp@igowo.de"

forwardings = ["%s@%s\t%s" % (f.source, f.domain, f.target) for f in Forwarding.objects.filter(active=True)]
forwardings += ["postmaster@%s\t%s" % (domain, POSTMASTER_ADDRESS) for domain in domains]
forwardings += ["abuse@%s\t%s" % (domain, ABUSE_ADDRESS) for domain in domains]
makefile("/etc/postfix/virtual_forwardings.new", "\n".join(forwardings) + "\n")
diff("/etc/postfix/virtual_forwardings", "/etc/postfix/virtual_forwardings.new", move_on_diff=True)
runprog(["/usr/sbin/postmap", "/etc/postfix/virtual_forwardings"])

### APACHE
# Generate an Apache monit-conf for every user who uses Apache
customers = set([x.owner for x in VirtualHost.objects.filter(apache_enabled=True)])
for customer in customers:
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
    if not os.path.exists(runpath + "/davlock"):
        mkdir(runpath + "/davlock", 0700)
    os.chown(runpath + "/davlock", uid, gid)
    
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
    monit_list += ["httpd-%s" % (username,)]

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

    makefile("/etc/logrotate.d/httpd-%s" % (username,), render_to_string("etc/logrotate.d/httpd", {"username": username}), 0755)
    makefile("/usr/sbin/apachectl-%s" % (username,), render_to_string("usr/bin/apachectl", {"username": username, "ipoffset": ipoffset}), 0755)
    runprog(["/usr/sbin/apachectl-%s" % (username,), "restart"])

sync(glob("/etc/logrotate.d/httpd-*"), ["/etc/logrotate.d/httpd-%s" % (c.user.username,) for c in customers], start_func=None, stop_func=remove)

### NGINX
makefile("/etc/nginx/conf/aliases", render_to_string("etc/nginx/conf/aliases", {"my_ip": settings.MY_IP, "aliases": Alias.objects.filter(active=True)}))

if os.path.exists("/etc/nginx/conf/sites"):
    rmtree("/etc/nginx/conf/sites")
mkdir("/etc/nginx/conf/sites", 0755)

for vh in VirtualHost.objects.filter(active=True):
    ipoffset = vh.owner.kundennr - 10000
    assert(ipoffset >= 0)
    ports = ("80",) if not vh.ssl_enabled else ("80", "443")
    for port in ports:
        config = render_to_string("etc/nginx/conf/sites/site", {
            "vh": vh,
            "port": port,
            "extra_aliases": " ".join([da.fqdn() for da in DirectAlias.objects.filter(active=True).filter(host=vh)]),
            "nginx_config": "\n".join(["    "+x for x in vh.nginx_config.replace("\r\n", "\n").split("\n")]),
            "ipoffset": ipoffset,
        })
        makefile("/etc/nginx/conf/sites/%s-%s" % (vh.fqdn(), port), config, strip_emptylines=True)

    # Fixup htdocs dir
    htdocs_dir = "/home/%s/www/%s/htdocs/" % (username, vh.fqdn())
    uid = getpwnam(vh.owner.user.username).pw_uid
    gid = getgrnam("users").gr_gid
    
    for dir in [os.path.realpath(htdocs_dir), os.path.realpath(os.path.join(htdocs_dir, "../"))]:
        if not os.path.exists(dir):
            print "WARNING: htdocs dir does not exist: %s" % (dir)
            mkdir(dir, 0755)

        statinfo = os.stat(dir)
        if statinfo.st_uid != uid or statinfo.st_gid != gid:
            chown(dir, vh.owner.user.username, "users")

runprog(["/etc/rc.d/nginx", "reload"])

### PHP
# Generate a PHP monit-conf for every user who uses PHP
for customer in set([x.owner for x in VirtualHost.objects.filter(enable_php=True)]):
    username = customer.user.username
    makefile("/etc/php/php-%s.sh" % (username,), render_to_string("etc/php/php.sh", {"username": username, "php_instances": 5}), 0755)
    makefile("/etc/php/php-%s.ini" % (username,), render_to_string("etc/php/php.ini", {
        "username": username,
        "sc": ServerConfig.objects.get(active=True),
        "virtualhosts": VirtualHost.objects.filter(owner=customer, enable_php=True),
        "extensions": PHPExtension.objects.all(),
    }))
    if not os.path.exists("/var/log/php-%s" % (username,)):
        mkdir("/var/log/php-%s" % (username,), 0755)
    chown("/var/log/php-%s" % (username,), username)
    makefile("/etc/logrotate.d/php-%s" % (username,), render_to_string("etc/logrotate.d/php", {"username": username}))
    makefile("/etc/monit.d/php-%s" % (username,), render_to_string("etc/monit.d/php", {"username": username}))
    monit_list += ["php-%s" % (username,)]
    monit_restart_list += ["php-%s" % (username,)]

makefile("/etc/php/php-pysk.sh", render_to_string("etc/php/php.sh", {"username": "pysk", "php_instances": 1}), 0755)
makefile("/etc/php/php-pysk.ini", render_to_string("etc/php/php.ini", {
    "username": "pysk",
    "sc": ServerConfig(default_php_config=PHPConfig.objects.get(name="production")),
    "virtualhosts": None,
    "extensions": PHPExtension.objects.all(),
}))
if not os.path.exists("/var/log/php-pysk"):
    mkdir("/var/log/php-pysk", 0755)
chown("/var/log/php-pysk", "pysk")
makefile("/etc/logrotate.d/php-pysk", render_to_string("etc/logrotate.d/php", {"username": "pysk"}))
makefile("/etc/monit.d/php-pysk", render_to_string("etc/monit.d/php", {"username": "pysk"}))
monit_list += ["php-pysk"]
monit_restart_list += ["php-pysk"]

customers = set([x.owner for x in VirtualHost.objects.filter(apache_enabled=True, enable_php=True)])
sync(glob("/etc/logrotate.d/php-*"), ["/etc/logrotate.d/php-%s" % (c.user.username,) for c in customers] + ["/etc/logrotate.d/php-pysk"], start_func=None, stop_func=remove)
sync(glob("/etc/php/php-*.sh"), ["/etc/php/php-%s.sh" % (c.user.username,) for c in customers] + ["/etc/php/php-pysk.sh"], start_func=None, stop_func=remove)
sync(glob("/etc/php/php-*.ini"), ["/etc/php/php-%s.ini" % (c.user.username,) for c in customers] + ["/etc/php/php-pysk.ini"], start_func=None, stop_func=remove)

for x in glob("/etc/php/conf.d/*"): remove(x)

### TARTARUS
if not os.path.exists("/var/spool/tartarus"):
    mkdir("/var/spool/tartarus", 0755)
if not os.path.exists("/etc/tartarus"):
    mkdir("/etc/tartarus", 0755)
makefile("/etc/tartarus/secret.key", render_to_string("etc/tartarus/secret.key"), 0700)
makefile("/etc/tartarus/home.conf", render_to_string("etc/tartarus/home.conf"), 0700)
makefile("/etc/tartarus/etc.conf", render_to_string("etc/tartarus/etc.conf"), 0700)
makefile("/etc/cron.d/tartarus", render_to_string("etc/cron.d/tartarus"), 0644)

### MONIT
def monit_kill(id):
    runprog(["/usr/bin/monit", "stop", id])
    remove("/etc/monit.d/%s" % (id,))
def monit_start(id):
    pass
sync([os.path.basename(x) for x in glob("/etc/monit.d/*")], monit_list, monit_start, monit_kill)

runprog(["/usr/bin/monit", "reload"])
for x in monit_restart_list: runprog(["/usr/bin/monit", "restart", x])
