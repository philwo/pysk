#!/bin/bash

rsync -a --exclude=copy.sh /opt/pysk/serverconfig/ /
chmod 0700 /root /root/.ssh /etc/monit.d
chmod 0600 /etc/monitrc /root/.pgpass /root/.ssh/*

