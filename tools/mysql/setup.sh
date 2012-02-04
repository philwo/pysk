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

# Remove anonymous users
mysql -e "DELETE FROM mysql.user WHERE User='';"

# Drop test database
mysql -e "DROP DATABASE test;"

# Remove privileges from test database
mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"

# Reload privileges tables
mysql -e "FLUSH PRIVILEGES;"

# Generate random password for MySQL
rootpw=`tr -cd '[:alnum:]' < /dev/urandom | head -c 12`

# Set root password
/usr/bin/mysqladmin -u root password $rootpw

cat > /root/.my.cnf <<OMG
[mysql]
user = root
password = $rootpw
host = localhost

[client]
user = root
password = $rootpw
host = localhost
OMG
chmod 0600 /root/.my.cnf

# Remove old root users
mysql --password="$rootpw" -e "DROP USER 'root'@'127.0.0.1';"
mysql --password="$rootpw" -e "DROP USER 'root'@'`hostname`';"

# Install Roundcube user + tables
mysql --password="$rootpw" -e "CREATE USER 'roundcube'@'localhost' IDENTIFIED BY 'BDSF7w3iurTs';"
mysql --password="$rootpw" -e "GRANT USAGE ON *.* TO 'roundcube'@'localhost' IDENTIFIED BY 'BDSF7w3iurTs';"
mysql --password="$rootpw" -e "CREATE DATABASE IF NOT EXISTS \`roundcube\`;"
mysql --password="$rootpw" -e "GRANT ALL PRIVILEGES ON \`roundcube\`.* TO 'roundcube'@'localhost';"
cat /opt/pysk/www/roundcube/SQL/mysql.initial.sql | sed s/InnoDB/MYISAM/gi | mysql --password="$rootpw" roundcube
