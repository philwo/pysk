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

export LANG="en_US.utf-8"

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
rootpw=`cat /root/.pgpass | grep localhost | cut -d':' -f5`
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
