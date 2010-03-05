#!/bin/bash

set -e
set -u

rm -f lists/*
pacman -Q > lists/haruhi

for i in `cat hosts`; do
    echo $i
    ssh $i pacman -Q > lists/$i
done

