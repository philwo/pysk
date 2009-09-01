#!/bin/bash

set -e
set -u

APIPASS=`cat /etc/pysk/apipass`

# Usual nginx configuration stuff
/opt/pysk/tools/nginx/nginx.py

# Aliases
wget --user=pysk --password=$APIPASS -O/etc/nginx/sites-available/aliases https://pysk.igowo.de/api/v0/vz/pear.igowo.de/aliases_nginx/ 2>/dev/null
ln -s /etc/nginx/sites-available/aliases /etc/nginx/sites-enabled/aliases

/etc/init.d/nginx reload

