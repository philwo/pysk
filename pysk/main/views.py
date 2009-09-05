# -*- coding: utf-8 -*-

import sys
import re
import csv
import imaplib
import email
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

from pysk.main.models import *
from pysk.vps.models import *

@user_passes_test(lambda u: u.is_superuser == True)
def sync(request):
	p = re.compile("35928,([0-9]+),logout")
	postdata = {"group_benutzerId": "pyskapi", "group_kennwort": "sENvHjd6ccna"}
	f = urlopen("https://www.collmex.de/cgi-bin/cgi.exe?35928,0,login", urlencode(postdata))

	for eachLine in f:
		m = re.search(p, eachLine)
		if m is not None:
			magicCookie = m.group(1)
			break

	if magicCookie is None:
		raise Exception, "Couldn't find the magic-cookie, maybe Collmex has changed the HTML design?"

	postdata = {"export": "Daten exportieren", "exp": "1", "group_kunden": "1"}
	f = urlopen("https://www.collmex.de/cgi-bin/cgi.exe?35928,%s,exp" % (magicCookie), urlencode(postdata))
	fbuf = f.read()
	fio = StringIO(fbuf)
	zf = ZipFile(fio, "r")

	csvbuf = zf.read("kunden.csv")
	csvio = StringIO(csvbuf)
	csvobj = csv.reader(csvio, delimiter=';', doublequote=True, escapechar=None, quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)

	headerRow = True
	for eachRecord in csvobj:
		if headerRow == True:
			headerRow = False
			continue

		c_id = eachRecord[1]

		# Skip "Allgemeiner Geschäftspartner"
		if c_id == "9999":
			continue

		try:
			u = User.objects.get(username=c_id)
		except ObjectDoesNotExist:
			email = eachRecord[17].decode("iso-8859-1")
			u = User.objects.create_user(c_id, email)

		try:
			c = u.get_profile()
		except ObjectDoesNotExist:
			c = Customer()
			c.user = u

		c.anrede = eachRecord[3].decode("iso-8859-1")
		c.titel = eachRecord[4].decode("iso-8859-1")
		u.first_name = eachRecord[5].decode("iso-8859-1")
		u.last_name = eachRecord[6].decode("iso-8859-1")
		c.firma = eachRecord[7].decode("iso-8859-1")
		c.abteilung = eachRecord[8].decode("iso-8859-1")
		c.strasse = eachRecord[9].decode("iso-8859-1")
		c.plz = eachRecord[10].decode("iso-8859-1")
		c.ort = eachRecord[11].decode("iso-8859-1")
		c.plz_postfach = eachRecord[12].decode("iso-8859-1")
		c.postfach = eachRecord[13].decode("iso-8859-1")
		c.land = eachRecord[14].decode("iso-8859-1")
		c.telefon = eachRecord[15].decode("iso-8859-1")
		c.telefax = eachRecord[16].decode("iso-8859-1")
		u.email = eachRecord[17].decode("iso-8859-1")
		c.kontonr = eachRecord[18].decode("iso-8859-1")
		c.blz = eachRecord[19].decode("iso-8859-1")
		c.iban = eachRecord[20].decode("iso-8859-1")
		c.bic = eachRecord[21].decode("iso-8859-1")
		c.bankname = eachRecord[22].decode("iso-8859-1")
		c.steuernummer = eachRecord[23].decode("iso-8859-1")
		c.ust_idnr = eachRecord[24].decode("iso-8859-1")

		# input = "6 14 Tage ohne Abzug", we're interested only in the integer ID
		tmp = eachRecord[25].decode("iso-8859-1")
		c.zahlungsbedingung = tmp[:tmp.find(" ")]

		c.rabattgruppe = eachRecord[26].decode("iso-8859-1")
		if c.rabattgruppe == "":
			c.rabattgruppe = None

		u.save()
		c.save()

	return HttpResponseRedirect("/admin/")

@user_passes_test(lambda u: u.is_superuser == True)
def import_cdr(request):
	M = imaplib.IMAP4("imap.igowo.de")
	M.login("outboxcdr@intra.igowo.de", "jgCjtfbr")
	M.select()
	typ, data = M.sort("DATE", "UTF-8", "UNSEEN")

	for num in data[0].split():
		typ, data = M.fetch(num, "(BODY.PEEK[])")
		msg = email.message_from_string(data[0][1])

		if msg["Subject"].find("Ihre CDR-Daten") != -1 and msg["From"] == "outbox AG <devnull@outbox.de>":
			for part in msg.walk():
				if part.get_content_type() != "text/plain":
					continue
				if not part.get_filename():
					continue
				if not part.get_filename().startswith("CDR-485-") or not part.get_filename().endswith(".csv"):
					continue

				csvio = StringIO(part.get_payload(decode=True))
				csvobj = csv.reader(csvio, delimiter=',', escapechar=None, quoting=csv.QUOTE_NONE, skipinitialspace=True)

				headerRow = True
				for eachRecord in csvobj:
					if headerRow == True:
						headerRow = False
						continue

					sa, sa_created = SipAccount.objects.get_or_create(name=eachRecord[0].decode("utf-8"))
					# TODO
					# if created == True:
					#	Somehow get information about the owner of the SipAccount ...
					sa.save()

					year, month, day = eachRecord[3].decode("utf-8").split("-")
					hour, minute, second = eachRecord[4].decode("utf-8").split(":")
					cdr, cdr_created = CDR.objects.get_or_create(
							fid = "OBX-" + eachRecord[9].decode("utf-8"),
							sip_account = sa,
							quellrufnr = eachRecord[1].decode("utf-8"),
							zielrufnr = eachRecord[2].decode("utf-8"),
							beginn = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)),
							dauer = int(eachRecord[5].decode("utf-8")),
							dest = Destination.objects.get(id=int(eachRecord[6].decode("utf-8"))),
							vk = Decimal(eachRecord[7].decode("utf-8")),
							ek = Decimal(eachRecord[8].decode("utf-8")))
					cdr.save()

					M.store(num, "+FLAGS", r"\Seen")

	M.close()
	M.logout()

	return HttpResponseRedirect("/admin/")

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

