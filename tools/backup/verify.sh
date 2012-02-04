#/bin/bash
# -*- coding: utf-8 -*-

# Copyright 2006 - 2012 Philipp Wollermann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e
set -u

FTP_PASSWORD="XXXXXXXX"
FTP_URL="ftp://XXXXX@88.198.42.117/duplicity/`hostname`/"
PASSPHRASE="XXXXXXXXXXXXXXX"

set -x

FTP_PASSWORD=$FTP_PASSWORD PASSPHRASE=$PASSPHRASE duplicity verify --encrypt-key "FA3B07B8" --sign-key "FA3B07B8" \
    --exclude /bin --exclude /boot --exclude /dev --exclude /lib --exclude /lib64 \
    --exclude /lost+found --exclude /media --exclude /mnt --exclude /opt \
    --exclude /proc --exclude /sbin --exclude /srv --exclude /sys --exclude /tmp \
    --exclude /usr --exclude /var/cache --exclude /var/lib/mysql --exclude /var/lib/postgres \
    --exclude /var/lib/postgres-8.3 --exclude /var/lock --exclude /var/tmp \
    --exclude "/var/log/*log.*" --exclude "/var/log/**/*log.*" --exclude /var/log/btmp \
    --exclude /var/lib/pacman --exclude /home/mirror --exclude /root/.cache/duplicity/ \
    --exclude /var/abs --exclude /swapfile \
    ${FTP_URL} /
