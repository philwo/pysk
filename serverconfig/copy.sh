#!/bin/bash

set -e
set -u

excludefile="/opt/pysk/etc/serverconfig/exclude/`hostname`"
rsyncopts="-rltDv --exclude copy.sh --exclude diff.sh"
mainuser=`grep "igowo user" /etc/passwd | head -n1 | cut -d":" -f1`
hostname=`hostname --fqdn`
ipaddress=`python -c "import socket;print socket.gethostbyaddr(socket.gethostname())[2][0]"`

if [ -s $excludefile ] ; then
	rsyncopts="$rsyncopts --exclude-from=$excludefile"
fi

. /opt/pysk/etc/serverconfig/default

if [ -e /opt/pysk/etc/serverconfig/$hostname ]; then
    . /opt/pysk/etc/serverconfig/$hostname
fi

#rm -rf /etc/monit.d
rsync $rsyncopts /opt/pysk/serverconfig/ /

echo "Fixing permissions"
chown root:root /
chmod 0755 /
chmod 0700 /root /root/.ssh /etc/monit.d
chmod 0600 /etc/monitrc /root/.pgpass /root/.ssh/*
chmod 0440 /etc/sudoers

chmod 0640 /etc/ssl/private/*
chmod 0600 /etc/ssl/private/star_igowo_de_combined.crt
chown root:sslkeys /etc/ssl/private/*

chown -R postgres:postgres /var/lib/postgres/data
chmod 0600 /var/lib/postgres/data/server.{crt,key}
chmod 0700 /var/lib/postgres/data

chown -R pysk:pysk /opt/pysk
chown -R root:root /opt/pysk/.hg
chmod 0711 /opt/pysk
chmod 0700 /opt/pysk/*
chmod -R u=rwX,g=rX,o= /opt/pysk/run /opt/pysk/secret /opt/pysk/www /opt/pysk/static
chown -R pysk:http /opt/pysk/run /opt/pysk/secret /opt/pysk/www /opt/pysk/static
chmod 0660 /opt/pysk/run/php.sock || /bin/true

echo "Fixing up configs"
sed -i s/XXXMAINUSERXXX/$mainuser/g /etc/httpd/conf/httpd.conf
sed -i s/XXXMAINUSERXXX/$mainuser/g /etc/php/php-fpm.conf
sed -i s/XXXMAINUSERXXX/$mainuser/g /etc/monit.d/php-fpm
sed -i s/XXXPHPCHILDRENXXX/5/g /etc/php/php-fpm.conf
sed -i s/XXXIPXXX/$ipaddress/g /etc/nginx/conf/pysk.conf
sed -i s/XXXHOSTNAMEXXX/$hostname/g /etc/nginx/conf/pysk.conf

ln -sf /etc/mysql/$mysql_conf /etc/mysql/my.cnf

MYSQLPW=`grep password /root/.my.cnf | sort -u | cut -d"=" -f2 | tr -d " "`
echo $MYSQLPW > /opt/pysk/secret/mysqlpw

echo "Removing pacnew files"
find /etc -name "*.pacnew" -delete
find /etc -name "*.pacsave" -delete
rm -f /etc/my.cnf /etc/mysql/*.cf

[ ! -f /usr/share/GeoIP/GeoIP.dat ] && /opt/pysk/tools/logfiles/update_geoip.sh

