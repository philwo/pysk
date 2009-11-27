# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from pysk.app.models import *
from pysk.vps.models import *
import cPickle
import hashlib
from time import time
from IPy import IP
import re

re_private_ip = re.compile(r'^(127\.|10\.)')

class PyskValidationException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

def genentries(resp, d):
    processed = [d.name]
    output = []

    # Google Apps For Your Domain integration
    if d.is_gafyd:
        output.append("; GOOGLE APPS - MX")
        output.append("@ IN MX 10 ASPMX.L.GOOGLE.COM.")
        output.append("@ IN MX 20 ALT1.ASPMX.L.GOOGLE.COM.")
        output.append("@ IN MX 20 ALT2.ASPMX.L.GOOGLE.COM.")
        output.append("@ IN MX 30 ASPMX2.GOOGLEMAIL.COM.")
        output.append("@ IN MX 30 ASPMX3.GOOGLEMAIL.COM.")
        output.append("@ IN MX 30 ASPMX4.GOOGLEMAIL.COM.")
        output.append("@ IN MX 30 ASPMX5.GOOGLEMAIL.COM.")
        output.append("")

        output.append("; GOOGLE APPS - SRV")
        output.append("_xmpp-server._tcp IN SRV 5 0 5269 xmpp-server.l.google.com.")
        output.append("_xmpp-server._tcp IN SRV 20 0 5269 xmpp-server1.l.google.com.")
        output.append("_xmpp-server._tcp IN SRV 20 0 5269 xmpp-server2.l.google.com.")
        output.append("_xmpp-server._tcp IN SRV 20 0 5269 xmpp-server3.l.google.com.")
        output.append("_xmpp-server._tcp IN SRV 20 0 5269 xmpp-server4.l.google.com.")
        output.append("_xmpp-client._tcp IN SRV 5 0 5222 xmpp-server.l.google.com.")
        output.append("_xmpp-client._tcp IN SRV 20 0 5222 xmpp-server1.l.google.com.")
        output.append("_xmpp-client._tcp IN SRV 20 0 5222 xmpp-server2.l.google.com.")
        output.append("_xmpp-client._tcp IN SRV 20 0 5222 xmpp-server3.l.google.com.")
        output.append("_xmpp-client._tcp IN SRV 20 0 5222 xmpp-server4.l.google.com.")
        output.append("_jabber._tcp IN SRV 5 0 5269 xmpp-server.l.google.com.")
        output.append("_jabber._tcp IN SRV 20 0 5269 xmpp-server1.l.google.com.")
        output.append("_jabber._tcp IN SRV 20 0 5269 xmpp-server2.l.google.com.")
        output.append("_jabber._tcp IN SRV 20 0 5269 xmpp-server3.l.google.com.")
        output.append("_jabber._tcp IN SRV 20 0 5269 xmpp-server4.l.google.com.")
        output.append("")
    else:
        # MX records
        output.append("; MX RECORDS")
        if (d.mx1 != ""): output.append("@ IN MX 10 %s" % (d.mx1,))
        if (d.mx2 != ""): output.append("@ IN MX 20 %s" % (d.mx2,))
        if (d.mx3 != ""): output.append("@ IN MX 30 %s" % (d.mx3,))
        output.append("")

        if d.jabber != "":
            output.append("; EJABBERD - SRV")
            output.append("_xmpp-server._tcp IN SRV 5 0 5269 %s" % (d.jabber,))
            output.append("_xmpp-client._tcp IN SRV 5 0 5222 %s" % (d.jabber,))
            output.append("_jabber._tcp IN SRV 5 0 5269 %s" % (d.jabber,))
            output.append("")

    output.append("; ON APPEND CUT HERE")

    dataset = NSEntry.objects.filter(domain=d)
    if dataset.count() > 0:
        output.append("; CUSTOM NS ENTRIES")
        for n in dataset:
            if n.type == "A":
                output.append("%s IN A %s" % (n.host if n.host else "@", n.value))
            elif n.type == "AAAA":
                output.append("%s IN AAAA %s" % (n.host if n.host else "@", n.value))
            elif n.type == "CNAME":
                output.append("%s IN CNAME %s" % (n.host if n.host else "@", n.value))
            elif n.type == "MX":
                output.append("%s IN MX %s %s" % (n.host if n.host else "@", n.priority, n.value))
            else:
                raise ValueError("Unknown NSEntry type %s" % (n.type,))
        output.append("")

    dataset = Alias.objects.filter(active=True).filter(domain=d)
    if dataset.count() > 0:
        output.append("; DOMAIN ALIASES")
        for a in dataset:
            output.append("; %s -> %s" % (a.fqdn(), a.target))
            output.append("%s IN A  %s" % (a.name if a.name else "@", settings.MY_IP))
            if a.www_alias:
                output.append("%s IN A %s" % ("www."+a.name if a.name else "www", settings.MY_IP))
        output.append("")

    dataset = VirtualHost.objects.filter(active=True).filter(domain=d)
    if dataset.count() > 0:
        output.append("; HOSTS")
        for vh in dataset:
            output.append("%s IN A %s" % (vh.name if vh.name else "@", vh.ipport.ip))
            output.append("%s IN A %s" % ("www."+vh.name if vh.name else "www", vh.ipport.ip))
        output.append("")

    dataset = DirectAlias.objects.filter(active=True).filter(domain=d)
    if dataset.count() > 0:
        output.append("; DIRECT ALIASES")
        for da in dataset:
            output.append("; %s -> %s" % (da.fqdn(), da.host.fqdn()))
            output.append("%s IN A %s" % (da.name if da.name else "@", da.host.ipport.ip))
        output.append("")
        
    dataset = Domain.objects.filter(active=True).filter(name__endswith="."+d.name)
    if dataset.count() > 0:
        output.append("; SUBDOMAINS")
        for sd in dataset:
            output.append("$ORIGIN %s." % (sd.name,))
            newoutput, newprocessed = genentries(resp, sd)
            output.extend(newoutput)
            processed.extend(newprocessed)
        output.append("")

    return output, processed

def bind(request):
    SOAmail = "info.igowo.de."
    refresh = 10000
    retry = 3600
    expire = 604800
    min = 86400

    resp = HttpResponse(mimetype="text/plain")

    domains = Domain.objects.filter(active=True)
    dlist = []
    dlist.extend(domains)
    dlist.sort(lambda x,y: x.name.count(".") - y.name.count("."))
    dprocessedlist = []
    zonefiles = {}

    for d in dlist:
        if d.name in dprocessedlist: continue
        output = []

        # SOA
        output.append("$TTL 3600")
        output.append("@ IN SOA %s %s ( SOASERIAL %d %d %d %d )" % ("ns1.igowo.de.", SOAmail, refresh, retry, expire, min))

        # NS records
        output.append("; NS RECORDS")
        if (d.ns1 != ""): output.append("@ IN NS %s" %(d.ns1,))
        if (d.ns2 != ""): output.append("@ IN NS %s" %(d.ns2,))
        if (d.ns3 != ""): output.append("@ IN NS %s" %(d.ns3,))
        if (d.ns4 != ""): output.append("@ IN NS %s" %(d.ns4,))
        if (d.ns5 != ""): output.append("@ IN NS %s" %(d.ns5,))
        if (d.ns6 != ""): output.append("@ IN NS %s" %(d.ns6,))
        output.append("")

        newoutput, newprocessed = genentries(resp, d)
        output.extend(newoutput)
        dprocessedlist.extend(newprocessed)

        # Get temporary zonefile
        tmpzone = "\n".join(output)

        # Compute digest to check if it was changed since last time
        #hash = hashlib.sha1(tmpzone).hexdigest()
        #if hash != d.zonehash:
        #    # Update the hash and generate a new serial (in save())
        #    d.zonehash = hash
        #    d.save()

        # Construct final zonefile
        #zonefiles[d.name] = tmpzone.replace("SOASERIAL", str(d.serial))
        zonefiles[d.name] = tmpzone

    resp.write(cPickle.dumps(zonefiles, cPickle.HIGHEST_PROTOCOL))
    return resp

def v0_aliases(request):
    """
    Wir generieren hier die Apache Config für die Weiterleitungen
    """
    resp = HttpResponse(mimetype="text/plain")

    for a in Alias.objects.filter(active=True):
        resp.write("<VirtualHost %s:80>\n" % (settings.MY_IP,))
        resp.write("\tServerName %s\n" % (a.fqdn(),))
        if a.www_alias:
            resp.write("\tServerAlias www.%s\n" % (a.fqdn(),))
        resp.write("\tServerAdmin support@igowo.de\n")
        resp.write("\tDocumentRoot /var/www/default/htdocs\n")
        resp.write("\tRedirect permanent / %s\n" % (a.target,))
        resp.write("</VirtualHost>\n\n");

    return resp

def v0_aliases_nginx(request):
    """
    Wir generieren hier die nginx Config für die Weiterleitungen
    """
    resp = HttpResponse(mimetype="text/plain")

    for a in Alias.objects.filter(active=True):
        if a.www_alias:
            server_name = "%s www.%s" % (a.fqdn(), a.fqdn())
        else:
            server_name = a.fqdn()

        # Append / if missing from target
        if not a.target.endswith("/"):
            a.target += "/"

        resp.write("server {\n")
        resp.write("\tlisten %s:80;\n" % (settings.MY_IP,))
        resp.write("\tserver_name %s;\n" % (server_name,))
        resp.write("\taccess_log off;\n")
        resp.write("\trewrite ^/(.*)$ %s$1 permanent;\n" % (a.target,))
        resp.write("}\n\n")
    return resp

def v0_nginx(request):
    """
    nginx configuration
    """
    resp = HttpResponse(mimetype="text/plain")

    vhosts = {}

    for vh in VirtualHost.objects.filter(active=True):
        username = vh.owner.user.username
        ipoffset = vh.owner.kundennr - 10000
        assert(ipoffset >= 0)
        htdocs_dir = "/home/%s/www/%s/htdocs" % (username, vh.fqdn())

        # Construct config common for both http and https server block
        output_commonconfig = []

        extra_aliases = ""
        for da in DirectAlias.objects.filter(active=True).filter(host=vh):
            extra_aliases += " %s" % (da.fqdn(),)
        
        output_commonconfig.append("\tserver_name %s www.%s %s;" % (vh.fqdn(), vh.fqdn(), extra_aliases.strip()))
        output_commonconfig.append("\troot %s/;" % (htdocs_dir,))
        output_commonconfig.append("\tindex index.php index.html index.htm;")
        output_commonconfig.append("\t")
        
        if vh.force_www == "strip":
            output_commonconfig.append("\t# Strip www from hostname")
            output_commonconfig.append("\tif ($host ~* www\.(.*)) {")
            output_commonconfig.append("\t\tset $host_without_www $1;")
            output_commonconfig.append("\t\trewrite ^(.*)$ http://$host_without_www$1 permanent;")
            output_commonconfig.append("\t}")
            output_commonconfig.append("\t")
        elif vh.force_www == "prepend":
            output_commonconfig.append("\t# Force www prefix")
            output_commonconfig.append("\tif ($host !~* www\.) {")
            output_commonconfig.append("\t\trewrite ^(.*)$ http://www.$host$1 permanent;")
            output_commonconfig.append("\t}")
            output_commonconfig.append("\t")
        
        if not vh.apache_enabled and vh.enable_php:
            output_commonconfig.append("\t# PHP (FastCGI)")
            output_commonconfig.append("\tlocation ~ ^(.+\.php)(.*)$ {")
            output_commonconfig.append("\t\tinclude /etc/nginx/conf/fastcgi_params;")
            output_commonconfig.append("\t\tfastcgi_index index.php;");
            output_commonconfig.append("\t\tfastcgi_split_path_info ^(.+\.php)(.*)$;");
            output_commonconfig.append("\t\tfastcgi_param SCRIPT_FILENAME %s$fastcgi_script_name;" % (htdocs_dir,));
            output_commonconfig.append("\t\tfastcgi_param PATH_INFO $fastcgi_path_info;");
            output_commonconfig.append("\t\tfastcgi_param PATH_TRANSLATED $document_root$fastcgi_path_info;");
            output_commonconfig.append("\t\tfastcgi_pass_header Authorization;");
            output_commonconfig.append("\t\tfastcgi_intercept_errors off;");
            output_commonconfig.append("\t\tif (-f $request_filename) {")
            output_commonconfig.append("\t\t\tfastcgi_pass unix:/tmp/php-%s.sock;" % (username,))
            output_commonconfig.append("\t\t}")
            output_commonconfig.append("\t}")
            output_commonconfig.append("\t")
        
        # Construct http and https server block
        output = []
        output.append("server {")
        output.append("\tlisten %s:80;" % (vh.ipport.ip,))
        output.append("\t")
        if vh.ssl_enabled and vh.ssl_force:
            output.append("\t# Force SSL")
            output.append("\trewrite ^(.*) https://$host$1 permanent;")
            output.append("\t")
        for line in output_commonconfig:
            output.append(line)
        if vh.apache_enabled:
            output.append("\t# HTTP Proxy to Apache")
            output.append("\tlocation / {")
            output.append("\t\tinclude /etc/nginx/conf/proxy_params;")
            output.append("\t\tproxy_pass http://127.0.%s.1:80/;" % (ipoffset,))
            output.append("\t}")
        output.append("\n".join(["\t"+x for x in vh.nginx_config.replace("\r\n", "\n").split("\n")]))
        output.append("\t")
        output.append("}\n")
        
        if vh.ssl_enabled:
            output.append("server {")
            output.append("\tlisten %s:443;" % (vh.ipport.ip,))
            output.append("\t")
            output.append("\t# SSL support")
            output.append("\tssl on;");
            output.append("\tssl_certificate %s;" % (vh.ssl_cert, ));
            if vh.ssl_key:
                output.append("\tssl_certificate_key %s;" % (vh.ssl_key, ));
            output.append("\t")
            for line in output_commonconfig:
                output.append(line)
            if vh.apache_enabled:
                output.append("\t# HTTP Proxy to Apache")
                output.append("\tlocation / {")
                output.append("\t\tinclude /etc/nginx/conf/proxy_params;")
                output.append("\t\tproxy_pass http://127.0.%s.1:81/;" % (ipoffset,))
                output.append("\t}")
            output.append("\n".join(["\t"+x for x in vh.nginx_config.replace("\r\n", "\n").split("\n")]))
            output.append("\t")
            output.append("}\n")

        vhosts[vh.fqdn()] = ["\n".join(output), username, htdocs_dir]
        
    resp.write(cPickle.dumps(vhosts, cPickle.HIGHEST_PROTOCOL))
    return resp

@login_required
def save(request):
    from subprocess import Popen, PIPE
    output = Popen(["/usr/bin/sudo", "/opt/pysk/tools/web.sh"], stdout=PIPE).communicate()[0]
    output += Popen(["/usr/bin/sudo", "/opt/pysk/tools/try.py"], stdout=PIPE).communicate()[0]
    return render_to_response("save.html", {"output": output}, context_instance=RequestContext(request))
