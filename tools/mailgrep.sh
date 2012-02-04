#!/bin/bash

cat `ls -1 /var/log/mail.log* | sort -r` | grep -v "connect from localhost.localdomain" | grep -v "Aborted login (no auth attempts)" | grep -v "postfix/anvil"
