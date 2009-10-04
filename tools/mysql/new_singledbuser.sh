#!/bin/bash

set -e
set -u
set -x

dbname=$1
dbpass=$2

mysql -e "CREATE USER '$dbname'@'localhost' IDENTIFIED BY '$dbpass';"
mysql -e "GRANT ALL PRIVILEGES ON $dbname.* TO '$dbname'@'localhost' IDENTIFIED BY '$dbpass';"
mysql -e "FLUSH PRIVILEGES;"
mysql -e "CREATE DATABASE $dbname;"

