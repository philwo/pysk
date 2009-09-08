#!/bin/bash

# Generate random password for Postgres
rootpw=`tr -cd '[:alnum:]' < /dev/urandom | head -c 12`
hostname=`hostname`

# Set password
psql -U postgres template1 -f - <<EOT
ALTER USER postgres WITH PASSWORD '${rootpw}';
EOT

# Store in .pgpass
cat > /root/.pgpass <<OMG
localhost:5432:*:postgres:${rootpw}
${hostname}:5432:*:postgres:${rootpw}
OMG
chmod 0600 /root/.pgpass

