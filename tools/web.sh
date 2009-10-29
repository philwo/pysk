#!/bin/bash

set -e
set -u

echo "IMAP / POP3 Server ..."
/opt/pysk/tools/dovecot/dovecot.sh || /bin/true
echo

echo "SMTP Server ..."
/opt/pysk/tools/postfix/postfix.sh || /bin/true
echo

echo "Apache Webserver ..."
/opt/pysk/tools/apache/apache.py
echo

echo "nginx Webserver ..."
/opt/pysk/tools/nginx/run.sh
echo

echo "Verschiedenes ..."
/opt/pysk/tools/passwd/passwd.py
echo

echo "Starte Webserver neu ..."
/usr/sbin/apachectl -t
/usr/sbin/apachectl restart
/etc/rc.d/nginx restart
echo

echo "Fertig!"

