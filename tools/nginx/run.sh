#!/bin/bash

set -e
set -u

APIPASS="W68p20YST5Iv6KGG"

# Usual nginx configuration stuff
/opt/pysk/tools/nginx/nginx.py

# Aliases
wget --user=pysk --password=$APIPASS -O/etc/nginx/sites-available/aliases https://localhost:8080/api/v0/vz/pear.igowo.de/aliases_nginx/ 2>/dev/null
ln -s /etc/nginx/sites-available/aliases /etc/nginx/sites-enabled/aliases

/etc/init.d/nginx reload

