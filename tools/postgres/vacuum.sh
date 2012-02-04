#!/bin/bash

set -e
set -u

databases=`psql -lAt | fgrep "|" | cut -d"|" -f1 | fgrep -v "template0"`
for db in $databases; do
    #echo "Vacuuming ${db} ..."
    psql -h localhost -U postgres -c "VACUUM ANALYZE;" -q ${db}
    psql -h localhost -U postgres -c "REINDEX DATABASE ${db};" -q ${db}
done
