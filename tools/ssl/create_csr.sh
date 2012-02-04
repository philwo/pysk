#!/bin/bash
# -*- coding: utf-8 -*-

# Copyright 2006 - 2012 Philipp Wollermann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
