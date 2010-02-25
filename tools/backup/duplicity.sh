#/bin/bash

FTP_PASSWORD="vzOQuQBd"
FTP_URL="ftp://48554@88.198.42.117/duplicity/`hostname`/"
PASSPHRASE="cY1V78sCkxeZ7jpReOCyixH8"

duplicity --full-if-older-than 6D --encrypt-key "FA3B07B8" --sign-key "FA3B07B8" \
    --exclude /sys --exclude /mnt --exclude /tmp --exclude /proc --exclude /dev \
    --exclude /var/lib/mysql --exclude /var/lib/postgres/data \
    / ${FTP_URL}
duplicity remove-all-but-n-full 2 --force ${FTP_URL}
duplicity cleanup --extra-clean --force ${FTP_URL}

