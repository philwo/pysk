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

#rm -rf /etc/monit.d
rsync $rsyncopts /opt/pysk/serverconfig/ /

echo "Fixing permissions"
chown root:root /
chmod 0755 /
chmod 0700 /root /root/.ssh /etc/monit.d
chmod 0600 /etc/monitrc /root/.pgpass /root/.ssh/* /etc/ssl/private/*
chmod 0440 /etc/sudoers

chown -R postgres:postgres /var/lib/postgres/data
chmod 0600 /var/lib/postgres/data/server.{crt,key}
chmod 0700 /var/lib/postgres/data

chown -R pysk:pysk /opt/pysk
chown -R root:root /opt/pysk/.hg
chmod 0711 /opt/pysk
chmod 0700 /opt/pysk/*
chmod -R u=rwX,g=rX,o= /opt/pysk/run /opt/pysk/secret /opt/pysk/www
chmod 0660 /opt/pysk/run/php.sock || /bin/true
chown -R pysk:http /opt/pysk/run /opt/pysk/secret /opt/pysk/www

echo "Fixing up configs"
sed -i s/XXXMAINUSERXXX/$mainuser/g /etc/httpd/conf/httpd.conf
sed -i s/XXXMAINUSERXXX/$mainuser/g /etc/php/php-fpm.conf
sed -i s/XXXPHPCHILDRENXXX/5/g /etc/php/php-fpm.conf
sed -i s/XXXIPXXX/$ipaddress/g /etc/nginx/conf/pysk.conf
sed -i s/XXXHOSTNAMEXXX/$hostname/g /etc/nginx/conf/pysk.conf

