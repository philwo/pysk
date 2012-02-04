#!/bin/bash

set -u

for i in `cat hosts`; do
    ssh root@$i "$@" &
done
