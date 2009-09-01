#!/bin/bash

set -e
set -u
set -x

echo "CONFROOT=https://files.igowo.de/vps/v0" > /etc/confroot
/opt/pysk/get_conf.sh
agr sysklogd klogd fail2ban
apt-get remove --purge sysklogd klogd fail2ban

cat > /etc/apt/sources.list <<'ROFL'
deb http://ubuntu.intergenia.de/ubuntu/ intrepid main restricted universe multiverse
deb http://ubuntu.intergenia.de/ubuntu/ intrepid-updates main restricted universe multiverse
deb http://ubuntu.intergenia.de/ubuntu/ intrepid-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu intrepid-security main restricted universe multiverse
#deb http://ubuntu.intergenia.de/ubuntu-prevu/intrepid/ ./
ROFL

apt-get update
apt-get dist-upgrade
apt-get autoremove
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)

agi syslog-ng apt-show-versions
/opt/pysk/get_conf.sh

echo "FIXING PREVU VERSIONS"
aptitude install lsb-base=3.2-14ubuntu2 lsb-release=3.2-14ubuntu2 libtool=2.2.4-0ubuntu4
apt-show-versions | grep prevu

apt-get clean
find /etc -name "*.dpkg*" -delete

remove-orphans
