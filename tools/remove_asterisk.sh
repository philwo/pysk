#!/bin/bash

set -e
set -u
set -x

echo "CONFROOT=https://files.igowo.de/vps/v0" > /etc/confroot
/opt/pysk/get_conf.sh

agr asterisk asterisk-prompt-de asterisk-config-custom libgpmg1 asterisk-sounds-main asterisk-sounds-extra
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)
apt-get -y remove --purge $(deborphan)

