#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys, os, os.path
from os import chmod, chown, rename
from stat import S_IMODE, ST_MODE
from optparse import OptionParser
from crypt import crypt
from datetime import datetime
from time import mktime
from string import letters, digits
from random import choice
from subprocess import Popen, PIPE
from shutil import copy2
import psycopg2, psycopg2.extras
import csv
import socket

def ensure_permissions(directory, perms):
    if not os.path.exists(directory):
        print "WARNING: directory did not exist: %s" % (directory,)
        os.makedirs(directory, perms)
    statinfo = os.stat(directory)
    if not S_IMODE(statinfo[ST_MODE]) == perms:
        print "WARNING: directory had wrong permissions: %s" % (directory,)
        os.chmod(directory, perms)

def ensure_uid_gid(directory, uid, gid):
    statinfo = os.stat(directory)
    if uid != -1:
        if not statinfo.st_uid == uid:
            print "WARNING: directory had wrong owner: %i != %i" % (uid, statinfo.st_uid)
            os.chown(directory, uid, -1)
    if gid != -1:
        if not statinfo.st_gid == gid:
            print "WARNING: directory had wrong group: %i != %i" % (gid, statinfo.st_gid)
            os.chown(directory, -1, gid)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    DATABASE_PASSWORD = 'z62VUW2m59Y69u99'
    db = psycopg2.connect("host='localhost' user='pysk' password='%s' dbname='pysk'" % (DATABASE_PASSWORD,))
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # /etc/passwd
    query = "SELECT u.username, u.password, u.id + 9999 AS uid, u.id + 9999 AS gid, 'igowo user' AS gecos, '/home/' || u.username AS home, '/bin/bash' AS shell, 'false' AS ftponly FROM auth_user u WHERE u.password LIKE 'crypt%' ORDER BY username"
    query = query + " UNION SELECT fu.suffix || '-' || u.username, u.password, u.id + 9999 AS uid, u.id + 9999 AS gid, 'igowo ftp user' AS gecos, fu.home, '/bin/false' AS shell, 'true' AS ftponly FROM vps_ftpuser fu, auth_user u WHERE fu.owner_id = u.id AND u.password LIKE 'crypt%' ORDER BY username" 
    cursor.execute(query)
    users = cursor.fetchall()

    #users_by_uid = dict([(x["uid"], x) for x in users])
    users_by_username = dict([(x["username"], x) for x in users])

    # Check if all passwords are encrypted correctly
    for u in users:
        assert(u[1].startswith("crypt$$1$"))
  
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
        if gid != 100 and (gid < 10000 or gid >= 20000):
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
    userlist = []
    for user_row in users:
        if user_row.ftponly == "true":
            continue
        groupname = user_row[0]
        fakepasswd = "x"
        gid = user_row[3]
        members = ""
        userlist.append(groupname)
        group_new.writerow((groupname, fakepasswd, gid, members))
    group_new.writerow(("users", "x", "100", ",".join(userlist)))
    
    # shadow.new
    for user_row in users:
        username = user_row[0]
        password = user_row[1][6:]
        days_since_1970 = int(mktime(datetime.now().timetuple()) / 86400)
        days_before_change_allowed = 0
        days_after_change_necessesary = 99999
        days_before_expire = 7
        shadow_new.writerow((username, password, days_since_1970, days_before_change_allowed, days_after_change_necessesary, days_before_expire, "", "", ""))

    # Finish up
    passwd_new_file.close()
    group_new_file.close()
    shadow_new_file.close()

    copy2("/etc/passwd", "/etc/passwd.old")
    copy2("/etc/group", "/etc/group.old")
    copy2("/etc/shadow", "/etc/shadow.old")
    rename("/etc/passwd.new", "/etc/passwd")
    rename("/etc/group.new", "/etc/group")
    rename("/etc/shadow.new", "/etc/shadow")

    print Popen(["/usr/sbin/pwck", "-s"], stdout=PIPE).communicate()[0]
    print Popen(["/usr/sbin/grpck", "-s"], stdout=PIPE).communicate()[0]

    print Popen(["diff", "-u", "/etc/passwd.old", "/etc/passwd"], stdout=PIPE).communicate()[0]
    print Popen(["diff", "-u", "/etc/group.old", "/etc/group"], stdout=PIPE).communicate()[0]
    print Popen(["diff", "-u", "/etc/shadow.old", "/etc/shadow"], stdout=PIPE).communicate()[0]
    
    for user_row in users:
        if user_row.ftponly == "true":
            continue
        user = user_row[0]
        uid = user_row[2]
        home = user_row[5]
        gid = 100 # "users" group
    
        print "Fixing permissions for user %s ..." % (user,)

        # /home/username
        ensure_permissions(home, 0755)
        ensure_uid_gid(home, uid, gid)

        # /home/username/www
        ensure_permissions(os.path.join(home, "www"), 0755)
        ensure_uid_gid(os.path.join(home, "www"), uid, gid)

if __name__ == "__main__":
  sys.exit(main())

