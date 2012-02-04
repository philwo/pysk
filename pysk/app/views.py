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
