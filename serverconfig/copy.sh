#!/bin/bash

set -e
set -u

EXCLUDEFILE="/opt/pysk/etc/serverconfig/exclude/`hostname`"
RSYNCOPTS="-a --exclude copy.sh"

if [ -s $EXCLUDEFILE ] ; then
	RSYNCOPTS="$RSYNCOPTS --exclude-from=$EXCLUDEFILE"
fi

rsync $RSYNCOPTS /opt/pysk/serverconfig/ /
chmod 0700 /root /root/.ssh /etc/monit.d
chmod 0600 /etc/monitrc /root/.pgpass /root/.ssh/*

