#!/bin/bash

set -e
set -u

hname=`hostname | sed 's/\./_/g'`

cat >/opt/pysk/serverconfig/etc/ssl/private/${hname}.cnf <<EOF
dir = /opt/pysk/serverconfig/etc/ssl/private
siteName = `hostname`

[ req ]
default_bits = 2048
default_keyfile = /opt/pysk/serverconfig/etc/ssl/private/${hname}.key
distinguished_name = req_distinguished_name
prompt = no

[ req_distinguished_name ]
CN = `hostname`
EOF

openssl req -new -nodes -config /opt/pysk/serverconfig/etc/ssl/private/${hname}.cnf -out /opt/pysk/serverconfig/etc/ssl/private/${hname}.csr

