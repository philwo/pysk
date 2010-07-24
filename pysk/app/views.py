# -*- coding: utf-8 -*-

import sys
import re
import csv
from StringIO import StringIO
from urllib import urlopen
from urllib import urlencode
from zipfile import ZipFile
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import smart_str

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

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


	return render_to_response("dashboard.html",
			{	"servers": servers,
				"domains": domains
			},
			context_instance=RequestContext(request))

