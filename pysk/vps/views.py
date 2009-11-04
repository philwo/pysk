# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.db import transaction
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from pysk.vps.models import *
import cPickle
import hashlib
from time import time
from IPy import IP

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

        #output.append("; GOOGLE APPS - SRV")
        #output.append("_xmpp-server._tcp IN SRV 5 0 5269 xmpp-server.l.google.com.")
        #output.append("_xmpp-server._tcp IN SRV 20 0 5269 xmpp-server1.l.google.com.")
        #output.append("_xmpp-server._tcp IN SRV 20 0 5269 xmpp-server2.l.google.com.")
        #output.append("_xmpp-server._tcp IN SRV 20 0 5269 xmpp-server3.l.google.com.")
        #output.append("_xmpp-server._tcp IN SRV 20 0 5269 xmpp-server4.l.google.com.")
        #output.append("_xmpp-client._tcp IN SRV 5 0 5222 xmpp-server.l.google.com.")
        #output.append("_xmpp-client._tcp IN SRV 20 0 5222 xmpp-server1.l.google.com.")
        #output.append("_xmpp-client._tcp IN SRV 20 0 5222 xmpp-server2.l.google.com.")
        #output.append("_xmpp-client._tcp IN SRV 20 0 5222 xmpp-server3.l.google.com.")
        #output.append("_xmpp-client._tcp IN SRV 20 0 5222 xmpp-server4.l.google.com.")
        #output.append("_jabber._tcp IN SRV 5 0 5269 xmpp-server.l.google.com.")
        #output.append("_jabber._tcp IN SRV 20 0 5269 xmpp-server1.l.google.com.")
        #output.append("_jabber._tcp IN SRV 20 0 5269 xmpp-server2.l.google.com.")
        #output.append("_jabber._tcp IN SRV 20 0 5269 xmpp-server3.l.google.com.")
        #output.append("_jabber._tcp IN SRV 20 0 5269 xmpp-server4.l.google.com.")
        #output.append("")

        output.append("; EJABBERD - SRV")
        output.append("_xmpp-server._tcp IN SRV 5 0 5269 mikuru.igowo.de.")
        output.append("_xmpp-client._tcp IN SRV 5 0 5222 mikuru.igowo.de.")
        output.append("_jabber._tcp IN SRV 5 0 5269 mikuru.igowo.de.")
        output.append("")
    else:
        # MX records
        output.append("; MX RECORDS")
        if (d.mx1 != ""): output.append("@ IN MX 10 %s" % (d.mx1,))
        if (d.mx2 != ""): output.append("@ IN MX 20 %s" % (d.mx2,))
        if (d.mx3 != ""): output.append("@ IN MX 30 %s" % (d.mx3,))
        output.append("")

    #output.append("; EMAIL")
    #output.append("mail IN A %s" % (settings.MY_IP,))
    #output.append("imap IN CNAME mail")
    #output.append("smtp IN CNAME mail")
    #output.append("pop IN CNAME mail")
    #output.append("")

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
            for ip in vh.ipports.all():
                hc = HostConfig.objects.get(host=vh, ipport=ip)
                if hc.publish_dns:
                    host_ip = ip.parent_ip.ip if ip.parent_ip else ip.ip
                    output.append("%s IN A %s" % (vh.name if vh.name else "@", host_ip))
                    #output.append("%s IN A %s" % ("ftp."+vh.name if vh.name else "ftp", host_ip))
                    output.append("%s IN A %s" % ("www."+vh.name if vh.name else "www", host_ip))
        output.append("")

    dataset = DirectAlias.objects.filter(active=True).filter(domain=d)
    if dataset.count() > 0:
        output.append("; DIRECT ALIASES")
        for da in dataset:
            hc = HostConfig.objects.get(host=da.host, ipport=da.ipport)
            if hc.publish_dns:
                ip = hc.ipport
                host_ip = ip.parent_ip.ip if ip.parent_ip else ip.ip
                output.append("; %s -> %s" % (da.fqdn(), da.host.fqdn()))
                output.append("%s IN A %s" % (da.name if da.name else "@", host_ip))
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
        # TODO implement non-wildcard redirecting here
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

def v0_apache(request):
    """
    Apache configuration for vserver
    """
    resp = HttpResponse(mimetype="text/plain")

    #host = settings.MY_HOSTNAME.split(".")[0]
    #domain = get_object_or_404(Domain, name=".".join(settings.MY_HOSTNAME.split(".")[1:]))

    #ips = []
    #vhosts = []
    all_vhosts = {}

    # For every IP of this server, which should be served by an apache
    for ip in IPAddress.objects.filter(configtype="apache"):
        if not ip.configtype in all_vhosts:
            all_vhosts[ip.configtype] = {}
        if not "vhosts" in all_vhosts[ip.configtype]:
            all_vhosts[ip.configtype]["vhosts"] = []
        if not "ips" in all_vhosts[ip.configtype]:
            all_vhosts[ip.configtype]["ips"] = set()
        
        vhosts = all_vhosts[ip.configtype]["vhosts"]
        ips = all_vhosts[ip.configtype]["ips"]
        
        # All VHosts which use this IP as an upstream parent (load balancer)
        children_hcs = HostConfig.objects.filter(ipport__parent_ip=ip)
        if children_hcs.count() > 0:
            raise PyskValidationException("HTTP forwarding using Apache is not supported anymore, please use nginx")

        # All VHosts which get directly served by this IP
        my_hcs = ip.hostconfig_set.all()
        
        # Get the number of VirtualHosts running on this IP
        hostcount = my_hcs.count() + children_hcs.count()

        if hostcount > 0:
            # If more than one host uses this IP:Port combination, we need name-based vhosts
            namehost = hostcount > 1
            ips.add((ip.ip, namehost, ip.port, ip.sslcert, ip.sslca, ip.sslkey))

            # For every virtualhost which uses this IP
            for vh in ip.virtualhost_set.filter(active=True).order_by("domain__name", "name"):
                # Associated host configuration
                vh_hcs = HostConfig.objects.filter(host=vh,ipport=ip)
                
                # This should return exactly one 
                if vh_hcs.count() > 1:
                    raise PyskValidationException("More than one hostconfig for VH/IP pair (%s, %s) found!" % (vh, ip))
                
                for hc in vh_hcs:
                    username = vh.owner.username
                    htdocs_dir = "/home/%s/www/%s/htdocs/" % (username, vh.fqdn())

                    output = []
                    output.append("<VirtualHost %s:%s>" % (ip.ip, ip.port))
                    output.append("ServerName %s" % (vh.fqdn(),))
                    output.append("ServerAdmin philipp@igowo.de")

                    extra_aliases = ""
                    for da in DirectAlias.objects.filter(active=True).filter(host=hc.host, ipport=hc.ipport):
                        extra_aliases += " %s" % (da.fqdn(),)

                    output.append("ServerAlias www.%s %s" % (vh.fqdn(), extra_aliases.strip()))
                    output.append("DocumentRoot %s" % (htdocs_dir,))
                    output.append("RewriteEngine On")
                    output.append("<Directory /home/%s/www/%s/htdocs/>" % (username, vh.fqdn()))
                    output.append("\tAllowOverride AuthConfig FileInfo Indexes Limit Options=FollowSymLinks,Indexes,MultiViews,SymLinksIfOwnerMatch")
                    output.append("\tOrder allow,deny")
                    output.append("\tallow from all")
                    output.append("</Directory>")
                    output.append(hc.config.replace("\r\n", "\n"))
                    if ip.parent_ip is not None:
                        output.append("RPAFenable On")
                        output.append("RPAFsethostname On")
                        #output.append("RPAFproxy_ips 127.0.0.1 %s" % (ip.parent_ip.ip))
                        output.append("RPAFproxy_ips 127.0.0.1")

                    # PHP via mod_php
                    output.append("AddHandler application/x-httpd-php .php")
                    output.append("AddHandler application/x-httpd-php-source .phps")

                    output.append("</VirtualHost>")
                    vhosts.append(("%s-%s-%s" % (vh.fqdn(), ip.ip, ip.port), "\n".join(output), username, htdocs_dir))
            
    # For every IP of this server, which should be served by an nginx load-balancer
    for ip in IPAddress.objects.filter(configtype="nginx"):
        if not ip.configtype in all_vhosts:
            all_vhosts[ip.configtype] = {}
        if not "vhosts" in all_vhosts[ip.configtype]:
            all_vhosts[ip.configtype]["vhosts"] = []
        if not "ips" in all_vhosts[ip.configtype]:
            all_vhosts[ip.configtype]["ips"] = set()
        
        vhosts = all_vhosts[ip.configtype]["vhosts"]
        ips = all_vhosts[ip.configtype]["ips"]
        
        # All VHosts which use this IP as an upstream parent (load balancer)
        children_hcs = HostConfig.objects.filter(ipport__parent_ip=ip)

        # Get the number of VirtualHosts running on this IP
        hostcount = children_hcs.count()

        if hostcount > 0:
            # If more than one host uses this IP:Port combination, we need name-based vhosts
            namehost = hostcount > 1
            ips.add((ip.ip, namehost, ip.port, ip.sslcert, ip.sslca, ip.sslkey))

            # Load-Balancer configs
            for hc in children_hcs:
                # We have to create a vhost which proxies requests made to
                # hc.host.fqdn() to hc.ipport.ip:hc.ipport.port
                vh = hc.host
                child_ip = hc.ipport
                parent_ip = child_ip.parent_ip
                output = []
                output.append("server {")
                output.append("\tlisten %s:%s;" % (parent_ip.ip, parent_ip.port))

                extra_aliases = ""
                for da in DirectAlias.objects.filter(active=True).filter(host=hc.host, ipport=hc.ipport):
                    extra_aliases += " %s" % (da.fqdn(),)

                output.append("\tserver_name %s www.%s %s;" % (vh.fqdn(), vh.fqdn(), extra_aliases.strip()))
                #output.append("\taccess_log off;")
                if parent_ip.sslcert:
                    output.append("\tssl on;");
                    output.append("\tssl_certificate %s;" % (parent_ip.sslcert, ));
                    if parent_ip.sslkey:
                        output.append("\tssl_certificate_key %s;" % (parent_ip.sslkey, ));
                output.append("\tlocation / {")
                output.append("\t\tproxy_pass http://%s:%s/;" % (child_ip.ip, child_ip.port))
                output.append("\t\tproxy_redirect off;")
                output.append("\t\tproxy_set_header   Host             $host;")
                output.append("\t\tproxy_set_header   X-Real-IP        $remote_addr;")
                output.append("\t\tproxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;")
                output.append("\t\tclient_max_body_size       1024m;")
                output.append("\t\tclient_body_buffer_size    128k;")
                output.append("\t\tproxy_send_timeout         300;")
                output.append("\t\tproxy_read_timeout         300;")
                output.append("\t\tproxy_buffer_size          4k;")
                output.append("\t\tproxy_buffers              4 32k;")
                output.append("\t\tproxy_busy_buffers_size    64k;")
                output.append("\t\tproxy_temp_file_write_size 64k;")
                output.append("\t}")
                output.append("}")
                
                vhosts.append(("%s-%s-%s" % (vh.fqdn(), parent_ip.ip, parent_ip.port), "\n".join(output)))
        
    resp.write(cPickle.dumps(all_vhosts, cPickle.HIGHEST_PROTOCOL))

    return resp

@user_passes_test(lambda u: u.is_superuser == True)
def migrate(request):
    return HttpResponseRedirect("/admin/")

@login_required
def save(request):
    from subprocess import Popen, PIPE
    output = Popen(["/usr/bin/sudo", "/opt/pysk/tools/web.sh"], stdout=PIPE).communicate()[0]
    return render_to_response("save.html", {"output": output}, context_instance=RequestContext(request))

