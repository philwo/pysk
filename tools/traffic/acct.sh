#!/bin/bash

set -e
set -u

IPTABLES=/sbin/iptables
VZLIST=/usr/sbin/vzlist

for VEID in `${VZLIST} -H -o hostname | sed 's/ //g'`; do
	# Parse inbound/outbound traffic into $VEIN $VEOUT
	eval `${IPTABLES} -nvx -L -Z ${VEID} | grep " 0.0.0.0/0 " | head -n2 | tr -s [:blank:] | cut -d" " -f3 | \
		awk '{traffic[NR] = $1} END {printf("VEIN=%-15d\nVEOUT=%-15d\n", traffic[1], traffic[2])}'`

	# Send the data to PostgreSQL
    psql -At -F $'\t' -U postgres -h localhost -c"SELECT * FROM update_traffic('$VEID', CURRENT_DATE, '$VEIN', '$VEOUT')" pysk > /dev/null
done

### Update Shorewall Config ###

cd /etc/shorewall
rm -f accounting.new rules.pysk.new

/opt/pysk/tools/traffic/shorewall.py > accounting.new
/opt/pysk/tools/traffic/shorewall_rules.py > rules.pysk.new

RESTART_SHOREWALL=0

diff -Bu accounting accounting.new ||
if [ -s "accounting.new" ]; then
	mv accounting.new accounting
    RESTART_SHOREWALL=1
fi

diff -Bu rules.pysk rules.pysk.new ||
if [ -s "rules.pysk.new" ]; then
	mv rules.pysk.new rules.pysk
    RESTART_SHOREWALL=1
fi

if [ $RESTART_SHOREWALL -eq 1 ]; then
	/sbin/shorewall restart
fi

rm -f accounting.new rules.pysk.new

