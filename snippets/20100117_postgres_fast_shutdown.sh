#!/bin/bash

set -e
set -u

echo -n "Enabling postgresql fast shutdown... "
cd /etc/rc.d
fgrep -- '-w stop"' postgresql >/dev/null && patch -p0 < /opt/pysk/snippets/20100117_postgres_fast_shutdown.diff &>/dev/null
fgrep -- '-w stop -m fast"' postgresql >/dev/null && echo "OK" || echo "FAIL"

