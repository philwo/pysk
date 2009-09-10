#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys, os, os.path
from optparse import OptionParser
import psycopg2, psycopg2.extras
from fileinput import FileInput
from subprocess import Popen, PIPE

def flatten(lst):
    for elem in lst:
        if type(elem) in (tuple, list):
            for i in flatten(elem):
                yield i
        else:
            yield elem

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
    
    query = "SELECT DISTINCT server_id, ip FROM vps_ipaddress WHERE server_id != 0 ORDER BY server_id, ip"
    cursor.execute(query)
    ips = {}

    for row in cursor.fetchall():
        if not row["server_id"] in ips:
            ips[row["server_id"]] = []
        ips[row["server_id"]].append(row["ip"])
    
    query = "SELECT DISTINCT s.id, i.ip FROM vps_server s, vps_ipaddress i WHERE s.main_ip_id = i.id ORDER BY s.id"
    cursor.execute(query)
    main_ips = dict([(x["id"], x["ip"]) for x in cursor.fetchall()])
    
    for server_id in ips:
        set_list = []
        current_config = open("/etc/vz/conf/%s.conf" % (server_id,), "rb").readlines()
        
        # IP addresses
        s_ips = ips[server_id]
        main_ip = main_ips[server_id]
        ips_without_main = sorted(filter(lambda x: x != main_ip, s_ips))
        ip_string = ("%s %s" % (main_ip, " ".join(ips_without_main))).strip()
        conf_string = 'IP_ADDRESS="%s"\n' % (ip_string, )

        if not conf_string in current_config:
            set_list += ["--ipdel", "all"] + list(flatten(("--ipadd", ip) for ip in [main_ip] + ips_without_main))

        if len(set_list) > 0:
            print Popen(["vzctl", "set", str(server_id), "--setmode", "restart"] + set_list + ["--save"], stdout=PIPE).communicate()[0]

if __name__ == "__main__":
    sys.exit(main())
