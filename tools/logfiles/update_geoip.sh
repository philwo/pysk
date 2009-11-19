#!/bin/bash

set -e
set -u

cd /usr/share/GeoIP
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
rm -f GeoIP.dat
gunzip GeoIP.dat.gz

