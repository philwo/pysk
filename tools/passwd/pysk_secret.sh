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

yes y | pwck

cat > /opt/pysk/secret/htpasswd.new <<'EOF'
pysk:04UnS7oSZEUVw
EOF

psql -At -F':' -U postgres -c"SELECT username, substring(password from 7) as password FROM auth_user WHERE password LIKE 'crypt\$%' ORDER BY username" pysk >> /opt/pysk/secret/htpasswd.new

grep "^philwo:" /opt/pysk/secret/htpasswd.new > /dev/null || echo 'philwo:$1$12345$12345678912345/123456.' >> /opt/pysk/secret/htpasswd.new

sort -u /opt/pysk/secret/htpasswd.new > /opt/pysk/secret/htpasswd.sorted

[ -f /opt/pysk/secret/htpasswd ] && diff -u /opt/pysk/secret/htpasswd /opt/pysk/secret/htpasswd.sorted || /bin/true
mv /opt/pysk/secret/htpasswd.sorted /opt/pysk/secret/htpasswd
rm -f /opt/pysk/secret/htpasswd.new
