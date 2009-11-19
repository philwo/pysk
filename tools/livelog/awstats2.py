#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys, os, MySQLdb, MySQLdb.cursors

def main(argv=None):
	if argv is None:
		argv = sys.argv

	db = MySQLdb.connect(host="db1.igowo.de", user="igowo_log_aw", passwd="LCQ3xrvBmbaV5pY7", db="igowo_log", charset="utf8", use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)
	cursor = db.cursor()

	# Generate DNS cache
	#print >> sys.stderr, "Generating DNS cache"
	query = "SELECT DISTINCT a.r_host, a.rdns FROM accesslog a WHERE a.rdns != a.r_host"
	cursor.execute(query)
	rows = cursor.fetchall()

	with open("/etc/awstats/dnscache.txt.new", "w") as f:
		for row in rows:
			f.write("%s %s\n" % (row["r_host"], row["rdns"]))
	os.rename("/etc/awstats/dnscache.txt.new", "/etc/awstats/dnscache.txt")

	# Call awstats

	# Fix permissions
	#chmod 0750 /var/lib/awstats
	#chown www-data.www-data /var/lib/awstats
	#chmod 0750 /var/lib/awstats/*
	#chown www-data.www-data /var/lib/awstats/*
	#chmod 0660 /var/lib/awstats/*/*
	#chown www-data.www-data /var/lib/awstats/*/*

if __name__ == "__main__":
	sys.exit(main())
