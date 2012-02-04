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

DBNAME=$1
DBMAINUSER=$2
DBMAINUSERPASS=$3

psql -U postgres template1 -f - <<EOT
CREATE ROLE $DBNAME NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOLOGIN;
CREATE ROLE $DBMAINUSER NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ENCRYPTED PASSWORD '$DBMAINUSERPASS';
GRANT $DBNAME TO $DBMAINUSER;
CREATE DATABASE $DBNAME WITH OWNER=$DBMAINUSER;
EOT

psql -U postgres $DBNAME -f - <<EOT
GRANT ALL ON SCHEMA public TO $DBMAINUSER WITH GRANT OPTION;
EOT
