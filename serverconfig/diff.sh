#!/bin/bash

EXCLUDEFILE="/opt/pysk/etc/serverconfig/exclude/`hostname`"
EXCLUDES=""

if [ -s $EXCLUDEFILE ] ; then
    for i in `cat $EXCLUDEFILE`; do
        $EXCLUDES="$EXCLUDES -x $i"
    done
fi

echo "diff -ur $EXCLUDES /opt/pysk/serverconfig/ / | grep -v 'Only in /' | less"

