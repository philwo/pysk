#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys, os, MySQLdb, MySQLdb.cursors
from datetime import datetime
from optparse import OptionParser

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = OptionParser()
    parser.add_option("-r", "--rdns", action="store_true", dest="rdns", help="Get logs with IPs resolved via RDNS", default=False)
    (options, args) = parser.parse_args(argv)

    if len(args) != 2:
        print >> sys.stderr, "Usage: resetid.py <date>"
        return 1

    date = datetime.strptime(args[1], "%Y-%m-%d")

    db = MySQLdb.connect(host="db1.igowo.de", user="igowo_log_reset", passwd="f6zqeBnwzuzvpMuc", db="igowo_log", charset="utf8", use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()

    query = "SELECT * FROM www_last_ids"
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        print "Resetting %s to %s ..." % (row["vhost"], date)
        query = "UPDATE www_last_ids SET last_id = (SELECT MIN(id) from accesslog WHERE vhost = %s AND date >= %s) WHERE vhost = %s"
        data = [row["vhost"], date, row["vhost"]]
        cursor.execute(query, data)

if __name__ == "__main__":
    sys.exit(main())
