#!/bin/bash

set -e
set -u

. /etc/conf.d/postgresql

# Let init script initialize most things
/etc/rc.d/postgresql start
sleep 3
/etc/rc.d/postgresql stop
sleep 3

# But then delete the default database and recreate with UTF8 charset
rm -rf $PGROOT/data
mkdir -p $PGROOT/data && chown postgres.postgres $PGROOT/data
su - postgres -c "/usr/bin/initdb -E UTF8 -D $PGROOT/data"

# Start postgres again
/etc/rc.d/postgresql start
sleep 3

# Generate random password for Postgres
rootpw=`tr -cd '[:alnum:]' < /dev/urandom | head -c 12`
hostname=`hostname`

# Set password
psql -U postgres template1 -f - <<EOT
ALTER USER postgres WITH PASSWORD '${rootpw}';

REVOKE ALL ON DATABASE template1 FROM public;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;

REVOKE ALL ON SCHEMA public FROM public;
GRANT ALL ON SCHEMA public TO postgres;

CREATE LANGUAGE plpgsql;

EOT

# Store in .pgpass
cat > /root/.pgpass <<OMG
localhost:5432:*:postgres:${rootpw}
${hostname}:5432:*:postgres:${rootpw}
OMG
chmod 0600 /root/.pgpass

