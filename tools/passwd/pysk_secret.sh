#!/bin/bash

set -e
set -u

yes y | pwck

cat > /opt/pysk/secret/htpasswd.new <<'EOF'
pysk:04UnS7oSZEUVw
EOF

psql -At -F':' -U postgres -c"SELECT username, substring(password from 7) as password FROM auth_user WHERE password LIKE 'crypt\$%' ORDER BY username" pysk >> /opt/pysk/secret/htpasswd.new

grep "^philwo:" /opt/pysk/secret/htpasswd.new > /dev/null || echo 'philwo:$1$23da4$ra1m6b0QAiYyxI/9XkB4F.' >> /opt/pysk/secret/htpasswd.new

sort -u /opt/pysk/secret/htpasswd.new > /opt/pysk/secret/htpasswd.sorted

[ -f /opt/pysk/secret/htpasswd ] && diff -u /opt/pysk/secret/htpasswd /opt/pysk/secret/htpasswd.sorted || /bin/true
mv /opt/pysk/secret/htpasswd.sorted /opt/pysk/secret/htpasswd
rm -f /opt/pysk/secret/htpasswd.new

