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
set -x

dbname=$1
dbpass=$2

mysql -e "CREATE USER '$dbname'@'localhost' IDENTIFIED BY '$dbpass';"
mysql -e "GRANT ALL PRIVILEGES ON $dbname.* TO '$dbname'@'localhost' IDENTIFIED BY '$dbpass';"
mysql -e "FLUSH PRIVILEGES;"
mysql -e "CREATE DATABASE $dbname;"
