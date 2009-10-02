#!/bin/bash

set -e
set -u

pacman -Rcs --noconfirm vi
rm -f /usr/bin/rview
pacman -S --noconfirm --force vim
ln -s /usr/bin/vim /usr/local/bin/vi
cp /opt/pysk/serverconfig/etc/vimrc /etc

