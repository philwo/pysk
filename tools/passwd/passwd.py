#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys, os, os.path
from os import chmod, chown, rename
from optparse import OptionParser
from crypt import crypt
from datetime import datetime
from time import mktime
from string import letters, digits
from random import choice
from subprocess import Popen, PIPE
import psycopg2, psycopg2.extras
import csv
import socket

def getsalt(chars = letters + digits, length=16):
    """Generate a random salt. Default length is 16.
       Originated from mkpasswd in Luma
    """
    salt = ""
    for i in range(int(length)):
        salt += choice(chars)
    return salt

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = OptionParser()
    #parser.add_option("-r", "--rdns", action="store_true", dest="rdns", help="Get logs with IPs resolved via RDNS", default=False)
    (options, args) = parser.parse_args(argv)

    #if len(args) != 2:
    #   print >> sys.stderr, "Usage: traffic.py <VirtualHost>"
    #   return 1

    DATABASE_PASSWORD = open("/etc/pysk/dbpass", "r").read().strip()
    db = psycopg2.connect("host='localhost' user='pysk' password='%s' dbname='pysk'" % (DATABASE_PASSWORD,))
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # /etc/passwd
    query = "SELECT DISTINCT p.username, p.password, p.uid, p.gid, p.gecos, p.home, p.shell FROM passwd_list p JOIN server_ip_user_list u ON p.username = u.username WHERE u.host = %s ORDER BY uid"
    cursor.execute(query, [socket.getfqdn()])
    users = cursor.fetchall()
    users_by_uid = dict([(x["uid"], x) for x in users])
    users_by_username = dict([(x["username"], x) for x in users])
  
    passwd_csv = csv.reader(open("/etc/passwd", "rb"), delimiter=":", quoting=csv.QUOTE_NONE)
    group_csv = csv.reader(open("/etc/group", "rb"), delimiter=":", quoting=csv.QUOTE_NONE)
    shadow_csv = csv.reader(open("/etc/shadow", "rb"), delimiter=":", quoting=csv.QUOTE_NONE)

    passwd_new_file = open("/etc/passwd.new", "w+b")
    group_new_file = open("/etc/group.new", "w+b")
    shadow_new_file = open("/etc/shadow.new", "w+b")
    passwd_new = csv.writer(passwd_new_file, delimiter=":", quoting=csv.QUOTE_NONE, lineterminator="\n")
    group_new = csv.writer(group_new_file, delimiter=":", quoting=csv.QUOTE_NONE, lineterminator="\n")
    shadow_new = csv.writer(shadow_new_file, delimiter=":", quoting=csv.QUOTE_NONE, lineterminator="\n")

    chmod("/etc/passwd.new", 0644)
    chmod("/etc/group.new", 0644)
    chmod("/etc/shadow.new", 0640)
    chown("/etc/passwd.new", 0, 0)
    chown("/etc/group.new", 0, 0)
    chown("/etc/shadow.new", 0, 0)

    # Read old passwd/group/shadow
    for row in passwd_csv:
        uid = int(row[2])
        if uid < 10000 or uid >= 20000:
            # User is an un-managed user, just copy it
            passwd_new.writerow(row)

    for row in group_csv:
        gid = int(row[2])
        if gid < 10000 or gid >= 20000:
            # User is an un-managed user, just copy it
            group_new.writerow(row)

    for row in shadow_csv:
        username = row[0]
        if not username in users_by_username:
            # User is an un-managed user, just copy it
            shadow_new.writerow(row)
    
    # Add our managed users from pysk
    # passwd.new
    for user_row in users:
        # Insert fake password, necessary for /etc/passwd
        username = user_row[0]
        fakepasswd = "x" # not user_row[1] !
        uid = user_row[2]
        gid = user_row[3]
        gecos = user_row[4]
        home = user_row[5]
        shell = user_row[6]
        passwd_new.writerow((username, fakepasswd, uid, gid, gecos, home, shell))

    # group.new
    for user_row in users:
        groupname = user_row[0]
        fakepasswd = "x"
        gid = user_row[3]
        members = ""
        group_new.writerow((groupname, fakepasswd, gid, members))
    
    # shadow.new
    for user_row in users:
        username = user_row[0]
        password = crypt(user_row[1], "$1$" + getsalt())
        days_since_1970 = int(mktime(datetime.now().timetuple()) / 86400)
        days_before_change_allowed = 0
        days_after_change_necessesary = 99999
        days_before_expire = 7
        shadow_new.writerow((username, password, days_since_1970, days_before_change_allowed, days_after_change_necessesary, days_before_expire, "", "", ""))

    # Finish up
    passwd_new_file.close()
    group_new_file.close()
    shadow_new_file.close()

    print Popen(["diff", "-u", "/etc/passwd", "/etc/passwd.new"], stdout=PIPE).communicate()[0]
    print Popen(["diff", "-u", "/etc/group", "/etc/group.new"], stdout=PIPE).communicate()[0]
    #print Popen(["diff", "-u", "/etc/shadow", "/etc/shadow.new"], stdout=PIPE).communicate()[0]

    rename("/etc/passwd.new", "/etc/passwd")
    rename("/etc/group.new", "/etc/group")
    rename("/etc/shadow.new", "/etc/shadow")

if __name__ == "__main__":
  sys.exit(main())

