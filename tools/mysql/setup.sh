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

# Remove old root users
mysql --password="$rootpw" -e "DROP USER 'root'@'127.0.0.1';"
mysql --password="$rootpw" -e "DROP USER 'root'@'`hostname`';"

# Install Roundcube user + tables
mysql --password="$rootpw" -e "CREATE USER 'roundcube'@'localhost' IDENTIFIED BY 'BDSF7w3iurTs';"
mysql --password="$rootpw" -e "GRANT USAGE ON *.* TO 'roundcube'@'localhost' IDENTIFIED BY 'BDSF7w3iurTs';"
mysql --password="$rootpw" -e "CREATE DATABASE IF NOT EXISTS \`roundcube\`;"
mysql --password="$rootpw" -e "GRANT ALL PRIVILEGES ON \`roundcube\`.* TO 'roundcube'@'localhost';"
cat /opt/pysk/www/roundcube/SQL/mysql.initial.sql | sed s/InnoDB/MYISAM/gi | mysql --password="$rootpw" roundcube

