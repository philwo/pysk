# -*- coding: utf-8 -*-

import sys
import re
import csv
import email
import imaplib

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from pysk.voip.models import *

# Create your views here.

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
