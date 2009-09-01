#!/bin/bash

set -e
set -u
set -x

echo "CONFROOT=https://files.igowo.de/vps/v0" > /etc/confroot
/opt/pysk/get_conf.sh

agr irb1.8 rdoc1.8 ruby1.8 rubygems rubygems1.8
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)

