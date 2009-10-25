#!/bin/bash

for i in `find / -name "*.db" | xargs file | grep Berkeley | fgrep -v "1.85" | cut -d":" -f1`; do db_upgrade -v $i; done

