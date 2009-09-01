#!/bin/bash

set -e
set -u

/opt/pysk/tools/apache/apache.py
/opt/pysk/tools/bind/bind.py
/opt/pysk/tools/dovecot/dovecot.sh
/opt/pysk/tools/nginx/run.sh
/opt/pysk/tools/openvz/openvz.py
/opt/pysk/tools/passwd/passwd.py
/opt/pysk/tools/postfix/postfix.sh

rndc reload

