#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys, socket
import psycopg2, psycopg2.extras
from optparse import OptionParser

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = OptionParser()
    #parser.add_option("-r", "--rdns", action="store_true", dest="rdns", help="Get logs with IPs resolved via RDNS", default=False)
    (options, args) = parser.parse_args(argv)

    #if len(args) != 2:
    #   print >> sys.stderr, "Usage: traffic.py <VirtualHost>"
    #   return 1

    DATABASE_PASSWORD = 'z62VUW2m59Y69u99'
    db = psycopg2.connect("host='db1.igowo.de' user='pysk' password='%s' dbname='pysk'" % (DATABASE_PASSWORD,))
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    query = "SELECT DISTINCT host, ip FROM server_ip_list"
    cursor.execute(query)

    print("""\
#
# Shorewall version 4 - Accounting File
#
#####################################################################################
#ACTION         CHAIN   SOURCE                  DESTINATION             PROTO   DEST            SOURCE  USER/   MARK
#                                                                       PORT(S)         PORT(S) GROUP
""")

    prevhost = None
    for row in cursor.fetchall():
        if row["host"] != prevhost and prevhost != None:
            print "COUNT %s eth0 venet0" % prevhost
            print "COUNT %s venet0 eth0" % prevhost
            print "DONE %s\n" % prevhost

        print "%s - venet0:%s eth0" % (row["host"], row["ip"])
        print "%s - eth0 venet0:%s" % (row["host"], row["ip"])

        prevhost = row["host"]
    print "COUNT %s eth0 venet0" % prevhost
    print "COUNT %s venet0 eth0" % prevhost
    print "DONE %s\n" % prevhost

    print "#LAST LINE -- ADD YOUR ENTRIES BEFORE THIS ONE -- DO NOT REMOVE"

if __name__ == "__main__":
    sys.exit(main())
