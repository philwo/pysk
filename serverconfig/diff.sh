#!/bin/bash

EXCLUDEFILE="/opt/pysk/etc/serverconfig/exclude/`hostname`"
EXCLUDES=""

if [ -s $EXCLUDEFILE ] ; then
    for i in `cat $EXCLUDEFILE`; do
        EXCLUDES="$EXCLUDES -x `basename $i`"
    done
fi

diff -wur -x php-fpm.conf -x known_hosts $EXCLUDES /opt/pysk/serverconfig/ / | grep -v 'Only in /' | less

