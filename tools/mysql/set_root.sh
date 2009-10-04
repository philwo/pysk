#!/bin/bash

set -e
set -u

password=`cat /root/.my.cnf  | grep password | head -n1 | cut -d"=" -f2 | tr -d " "`
echo "Password on `hostname` is $password"

set -x
set +e

mysql -e "CREATE USER 'root'@'localhost' IDENTIFIED BY '$password';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '$password' WITH GRANT OPTION;"
mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host!='localhost';"
mysql -e "FLUSH PRIVILEGES;"

