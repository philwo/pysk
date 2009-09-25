#!/bin/bash

set -e
set -u

pacman -Rcs --noconfirm vi
rm -f /usr/bin/rview
pacman -S --noconfirm vim
ln -s /usr/bin/vim /usr/local/bin/vi

