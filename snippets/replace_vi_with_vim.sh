#!/bin/bash

set -e
set -u

pacman -Rcs vi
rm -f /usr/bin/rview
pacman -S vim
ln -s /usr/bin/vim /usr/local/bin/vi

