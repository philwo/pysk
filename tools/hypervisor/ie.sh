#!/bin/bash

set -u

for i in `cat hosts`; do
    echo "###### $i ######"
    ssh root@$i "pacman -Sy --noconfirm --noprogressbar --needed pacman; pacman -S --noconfirm --noprogressbar --needed $@"
done
