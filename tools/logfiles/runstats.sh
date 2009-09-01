#!/bin/bash

set -e
set -u

/opt/pysk/logfiles/rdns.py
/opt/pysk/logfiles/awstats.py
/usr/share/doc/awstats/examples/awstats_updateall.pl now -awstatsprog=/usr/lib/cgi-bin/awstats.pl > /dev/null
chmod 0750 /var/lib/awstats
chown 5000:5000 /var/lib/awstats
chmod 0750 /var/lib/awstats/*
chown 5000:5000 /var/lib/awstats/*
chmod 0660 /var/lib/awstats/*/*
chown 5000:5000 /var/lib/awstats/*/*

