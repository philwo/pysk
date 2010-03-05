#!/bin/bash

set -u

for i in `cat hosts`; do
    scp $1 root@$i:$2
done

