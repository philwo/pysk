# -*- coding: utf-8 -*-

import re
from urllib import urlopen

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import user_passes_test

from pysk.app.models import *
from pysk.vps.models import *


@user_passes_test(lambda u: u.is_superuser == True)
def dashboard(request):
    servers = Server.objects.filter(active=True)
    domains = Domain.objects.filter(active=True)

    re_apache = re.compile(r"Server Version: (.*)</")

    for s in servers:
        s.services = {}
        #s.services["asterisk"] = "OK"

        for ip in s.ipaddress_set.all():
            try:
                lines = urlopen("http://%s/server-status/" % (ip.ip,)).readlines()
                s.services["apache (%s)" % (ip.ip,)] = re_apache.search("".join(lines)).group(1)
            except:
                s.services["apache (%s)" % (ip.ip,)] = '<span style="background-color:red">FAILED</span>'

    return render_to_response("dashboard.html", {
        "servers": servers,
        "domains": domains
    }, context_instance=RequestContext(request))
