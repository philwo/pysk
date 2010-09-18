#!/bin/bash

set -e
set -u

excludefile="/opt/pysk/etc/serverconfig/exclude/`hostname`"
rsyncopts="-rltD --exclude copy.sh --exclude diff.sh"
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

chown -R root:root /etc/dovecot/*.conf*  /etc/dovecot/conf.d/*
chmod 0644 /etc/dovecot/*.conf* /etc/dovecot/conf.d/*

chown -R postgres:postgres /var/lib/postgres/data
chmod 0600 /var/lib/postgres/data/server.{crt,key}
chmod 0700 /var/lib/postgres/data

chown -R pysk:pysk /opt/pysk
chown -R root:root /opt/pysk/.hg /opt/pysk/vendors/django/.hg /opt/pysk/vendors/django-extensions/.hg
chmod 0711 /opt/pysk
chmod 0700 /opt/pysk/*
chmod -R u=rwX,g=rX,o= /opt/pysk/secret /opt/pysk/www /opt/pysk/static
chown -R pysk:http /opt/pysk/secret /opt/pysk/www /opt/pysk/static

echo "Fixing up configs"
newaliases
postmap /etc/postfix/rbl_override
sed -i s/XXXIPXXX/$ipaddress/g /etc/nginx/conf/pysk.conf
sed -i s/XXXHOSTNAMEXXX/$hostname/g /etc/nginx/conf/pysk.conf

ln -sf /etc/mysql/$mysql_conf /etc/mysql/my.cnf
ln -sf /etc/postfix/$postfix_conf /etc/postfix/main.cf

echo -n "Enabling postgresql fast shutdown... "
cd /etc/rc.d
fgrep -- '-w stop"' postgresql >/dev/null && patch -p0 < /opt/pysk/snippets/20100117_postgres_fast_shutdown.diff &>/dev/null
fgrep -- '-w stop -m fast"' postgresql >/dev/null && echo "OK" || echo "FAIL"

MYSQLPW=`grep password /root/.my.cnf | sort -u | cut -d"=" -f2 | tr -d " "`
echo $MYSQLPW > /opt/pysk/secret/mysqlpw

[ -e /swapfile ] && echo "/swapfile              none          swap      sw                                                              0      0" >> /etc/fstab
swapon -a

echo "Removing pacnew files"
find /etc -name "*.pacnew" -delete || /bin/true
find /etc -name "*.pacsave" -delete || /bin/true
rm -f /etc/my.cnf /etc/mysql/*.cf || /bin/true

[ ! -f /usr/share/GeoIP/GeoIP.dat ] && /opt/pysk/tools/logfiles/update_geoip.sh

exit 0

