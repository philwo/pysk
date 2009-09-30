#!/bin/bash

set -e
set -u

VMAILUID=`stat --printf="%u" /home/vmail/`
VMAILGID=`stat --printf="%g" /home/vmail/`

cd /etc/dovecot
rm -f passwd.new passwd.sort
touch passwd passwd.new passwd.sort

IFS=`echo -e "\t\n"`
psql -At -F $'\t' -U postgres -h localhost -c'SELECT * FROM dovecot_passwd' pysk  | while read USER PASSWORD QUOTA HOME; do
	echo "$USER:$PASSWORD:$VMAILUID:$VMAILGID::$HOME::$QUOTA" >> passwd.new
done

sort passwd.new > passwd.sort

diff -Bu passwd passwd.sort ||
if [ -s "passwd.sort" ]; then
	# We need a \n at the end of the last line!
	echo >> passwd.sort
	mv passwd passwd.old
	mv passwd.sort passwd
	chmod 0600 passwd
fi
rm -f passwd.new passwd.sort

