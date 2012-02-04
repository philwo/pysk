#/bin/bash

set -e
set -u

FTP_PASSWORD="XXXXXXXX"
FTP_URL="ftp://XXXXX@88.198.42.117/duplicity/`hostname`/"
PASSPHRASE="XXXXXXXXXXXXXXX"

set -x

FTP_PASSWORD=$FTP_PASSWORD PASSPHRASE=$PASSPHRASE duplicity $@ --encrypt-key "FA3B07B8" --sign-key "FA3B07B8" ${FTP_URL}
