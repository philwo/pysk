#!/bin/bash

set -e
set -u

/opt/pysk/tools/dovecot/dovecot.sh || /bin/true
/opt/pysk/tools/postfix/postfix.sh || /bin/true

/opt/pysk/tools/apache/apache.py
/opt/pysk/tools/nginx/nginx.py
/opt/pysk/tools/passwd/passwd.py

/usr/sbin/apachectl graceful
/etc/rc.d/nginx reload

