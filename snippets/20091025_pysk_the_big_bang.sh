#!/bin/bash

set -e
set -u
set -x

cd /opt/pysk
hg pull -u
monit stop httpd
monit stop nginx
pacman -Syu --noconfirm
pacman -S --noconfirm openssl apache mod_rpaf mod_wsgi php php-apache php-apc php-cgi php-curl php-enchant php-gd php-gmp php-intl php-mcrypt php-pgsql php-pspell php-sqlite php-tidy php-xsl
pacman -S --noconfirm openssl apache mod_rpaf mod_wsgi php php-apache php-apc php-cgi php-curl php-enchant php-gd php-gmp php-intl php-mcrypt php-pgsql php-pspell php-sqlite php-tidy php-xsl
monit restart pysk
/opt/pysk/snippets/20091025_pysk_add_unixuser.sh
psql pysk < /opt/pysk/snippets/20091025_pysk_db_drop_server.sql
/opt/pysk/serverconfig/copy.sh
monit start nginx
monit reload
/opt/pysk/tools/web.sh
monit start httpd
/etc/rc.d/nginx restart
tail -f /var/log/nginx/error.log /var/log/httpd/error.log

