#/bin/bash

set -e
set -u

FTP_PASSWORD="vzOQuQBd"
FTP_URL="ftp://48554@88.198.42.117/duplicity/`hostname`/"
PASSPHRASE="cY1V78sCkxeZ7jpReOCyixH8"

set -x

FTP_PASSWORD=$FTP_PASSWORD PASSPHRASE=$PASSPHRASE duplicity $@ --encrypt-key "FA3B07B8" --sign-key "FA3B07B8" ${FTP_URL}

