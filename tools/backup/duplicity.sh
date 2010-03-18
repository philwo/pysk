#/bin/bash

set -e
set -u

FTP_HOST="88.198.42.117"
FTP_USER="48554"
FTP_PASSWORD="vzOQuQBd"
FTP_URL="ftp://$FTP_USER@$FTP_HOST/duplicity/`hostname`/"
PASSPHRASE="cY1V78sCkxeZ7jpReOCyixH8"

set -x

lftp -c "open $FTP_HOST && login $FTP_USER $FTP_PASSWORD && cd duplicity && mkdir `hostname`" &> /dev/null || /bin/true

FTP_PASSWORD=$FTP_PASSWORD PASSPHRASE=$PASSPHRASE duplicity --full-if-older-than 6D --encrypt-key "FA3B07B8" --sign-key "FA3B07B8" -v8 \
    --gpg-options='--compress-algo=bzip2 --bzip2-compress-level=9' --asynchronous-upload \
    --exclude /bin --exclude /boot --exclude /dev --exclude /lib --exclude /lib64 \
    --exclude /lost+found --exclude /media --exclude /mnt --exclude /opt \
    --exclude /proc --exclude /sbin --exclude /srv --exclude /sys --exclude /tmp \
    --exclude /usr --exclude /var \
    --exclude /home/mirror --exclude /root/.cache/duplicity/ \
    / ${FTP_URL}
FTP_PASSWORD=$FTP_PASSWORD PASSPHRASE=$PASSPHRASE duplicity remove-all-but-n-full 2 --force ${FTP_URL}
FTP_PASSWORD=$FTP_PASSWORD PASSPHRASE=$PASSPHRASE duplicity cleanup --extra-clean --force ${FTP_URL}

