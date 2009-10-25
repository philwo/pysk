#!/bin/bash

set -e
set -u

APIPASS="W68p20YST5Iv6KGG"

# Usual nginx configuration stuff
/opt/pysk/tools/nginx/nginx.py

# Aliases
wget --user=pysk --password=$APIPASS -O/etc/nginx/conf/sites-available/aliases https://`hostname`/api/v0/vz/pear.igowo.de/aliases_nginx/ 2>/dev/null
ln -s /etc/nginx/conf/sites-available/aliases /etc/nginx/conf/sites-enabled/aliases

#/etc/rc.d/nginx reload

