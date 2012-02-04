#!/bin/bash

set -e
set -u

cd /root/pacman &&
./se.sh "/bin/bash -l /opt/pysk/tools/backup/mysql.sh; /bin/bash -l /opt/pysk/tools/backup/psql.sh; /bin/bash -l /opt/pysk/tools/backup/duplicity.sh"
