#!/bin/bash

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

