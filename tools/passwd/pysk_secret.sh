#!/bin/bash

set -e
set -u

cat > /opt/pysk/secret/htpasswd.new <<'EOF'
pysk:04UnS7oSZEUVw
philwo:$1$23da4$ra1m6b0QAiYyxI/9XkB4F.
EOF

psql -At -F':' -U postgres -c"SELECT username, substring(password from 7) as password FROM auth_user WHERE password LIKE 'crypt\$%' ORDER BY username" pysk >> /opt/pysk/secret/htpasswd.new

diff -u /opt/pysk/secret/htpasswd /opt/pysk/secret/htpasswd.new || /bin/true
mv /opt/pysk/secret/htpasswd.new /opt/pysk/secret/htpasswd

