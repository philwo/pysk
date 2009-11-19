#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys, socket, MySQLdb, MySQLdb.cursors
from optparse import OptionParser

def main(argv=None):
	if argv is None:
		argv = sys.argv

	parser = OptionParser()
	parser.add_option("-r", "--rdns", action="store_true", dest="rdns", help="Get logs with IPs resolved via RDNS", default=False)
	(options, args) = parser.parse_args(argv)

	if len(args) != 2:
		print >> sys.stderr, "Usage: getlog.py <VirtualHost>"
		return 1

	db = MySQLdb.connect(host="db1.igowo.de", user="igowo_log_getlog", passwd="pAG9UztZxJjpTZSu", db="igowo_log", charset="utf8", use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)
	cursor = db.cursor()

	# Check if vhost exists
	vhost = args[1]
	query = "SELECT DISTINCT vhost FROM accesslog WHERE vhost = %s"
	data = [vhost]
	cursor.execute(query, data)

	if not cursor.rowcount > 0:
		print >> sys.stderr, "Error: Virtualhost %s not found in database!" % (vhost,)
		return 2

	# Get last id of vhost
	query = "SELECT last_id FROM www_last_ids WHERE vhost = %s"
	data = [vhost]

	cursor.execute(query, data)
	if cursor.rowcount > 0:
		last_id = cursor.fetchall()[0]["last_id"]
	else:
		last_id = 0

	# Get log-lines
	i = 0
	max_id = last_id
	while True:
		query = "SELECT a.id, INET_NTOA(a.r_host) as r_host, a.rdns, a.r_user, a.date, a.request, a.status, a.response_size, a.referer, a.user_agent FROM accesslog a WHERE a.vhost = %s AND a.id > %s ORDER BY date ASC LIMIT %s, 100000"
		data = [vhost, last_id, i]
		cursor.execute(query, data)

		i += cursor.rowcount

		for line in cursor.fetchall():
			cid = int(line["id"])
			if cid > max_id: max_id = cid

			if options.rdns:
				# Check if we have an RDNS lookup for this host
				if line["rdns"] is None:
					# Try to resolve it
					try:
						host = socket.gethostbyaddr(line["r_host"])[0]
					except socket.herror:
						# If we can't resolve it, use the IP
						host = line["r_host"]
				else:
					host = line["rdns"]
			else:
				host = line["r_host"]

			logline = u'%s - %s [%s +0000] "%s" %s %s "%s" "%s"' % (host, line["r_user"], line["date"].strftime("%d/%b/%Y:%H:%M:%S"), line["request"], line["status"], line["response_size"], line["referer"], line["user_agent"])
			print logline.encode("utf-8")
		
		if cursor.rowcount < 100000:
			break;

	# Update last_id
	query = "INSERT INTO www_last_ids (vhost, last_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE last_id = %s"
	data = [vhost, max_id, max_id]
	cursor.execute(query, data)

if __name__ == "__main__":
	sys.exit(main())

