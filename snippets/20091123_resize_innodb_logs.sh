#!/bin/bash

/etc/rc.d/mysqld stop
sleep 5
rm -f /var/lib/mysql/ib_logfile*
/etc/rc.d/mysqld start

