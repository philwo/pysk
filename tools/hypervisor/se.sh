#!/bin/bash

set -u

for i in `cat hosts`; do
    echo "###### $i ######"
    ssh -t root@$i "$@"
done

