#!/bin/bash

set -u

for i in `cat hosts`; do
    ssh root@$i "pacman -Sy --noconfirm --noprogressbar --needed pacman; pacman -S --noconfirm --noprogressbar --needed $@"
done

