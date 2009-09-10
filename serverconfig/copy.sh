#!/bin/bash

set -e
set -u

EXCLUDEFILE="/opt/pysk/etc/serverconfig/exclude/`hostname`"
RSYNCOPTS="-a --exclude copy.sh --exclude diff.sh"
MAINUSER=`grep "igowo user" /etc/passwd | head -n1 | cut -d":" -f1`

if [ -s $EXCLUDEFILE ] ; then
	RSYNCOPTS="$RSYNCOPTS --exclude-from=$EXCLUDEFILE"
fi

#rm -rf /etc/monit.d
rsync $RSYNCOPTS /opt/pysk/serverconfig/ /

echo "Fixing permissions"
chmod 0700 /root /root/.ssh /etc/monit.d
chmod 0600 /etc/monitrc /root/.pgpass /root/.ssh/*
chown -R postgres:postgres /var/lib/postgres/data
chmod 0600 /var/lib/postgres/data/server.{crt,key}
chmod 0700 /var/lib/postgres/data
chmod 0600 /etc/ssl/private/*

echo "Fixing up httpd.conf"
sed -i s/MAINUSER/$MAINUSER/g /etc/httpd/conf/httpd.conf
sed -i s/MAINUSER/$MAINUSER/g /etc/php/php-fpm.conf

