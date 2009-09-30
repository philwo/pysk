#!/bin/bash

set -e
set -u

cd /etc/postfix

rm -f virtual_mailboxes.new virtual_forwardings.new virtual_domains.new
touch virtual_mailboxes.new virtual_forwardings.new virtual_domains.new
touch virtual_mailboxes virtual_forwardings virtual_domains roleaccounts

postfix set-permissions 2>/dev/null

# virtual_mailboxes
psql -At -F $'\t' -U postgres -h localhost -c'SELECT * FROM postfix_virtual_mailboxes' pysk | sort > virtual_mailboxes.new

# virtual_domains
psql -At -F $'\t' -U postgres -h localhost -c'SELECT * FROM postfix_virtual_domains' pysk | sort > virtual_domains.new

# virtual_forwardings
psql -At -F $'\t' -U postgres -h localhost -c'SELECT * FROM postfix_virtual_forwardings' pysk | sort > virtual_forwardings.new

diff -Bu virtual_mailboxes virtual_mailboxes.new ||
if [ -s "virtual_mailboxes.new" ]; then
	echo >> virtual_mailboxes.new
	mv virtual_mailboxes virtual_mailboxes.old
	mv virtual_mailboxes.new virtual_mailboxes
	postmap virtual_mailboxes
fi
rm -f virtual_mailboxes.new

diff -Bu virtual_domains virtual_domains.new ||
if [ -s "virtual_domains.new" ]; then
	echo >> virtual_domains.new
	mv virtual_domains virtual_domains.old
	mv virtual_domains.new virtual_domains
	postmap virtual_domains
fi
rm -f virtual_domains.new

diff -Bu virtual_forwardings virtual_forwardings.new ||
if [ -s "virtual_forwardings.new" ]; then
	echo >> virtual_forwardings.new
	mv virtual_forwardings virtual_forwardings.old
	mv virtual_forwardings.new virtual_forwardings
	postmap virtual_forwardings
fi
rm -f virtual_forwardings.new

# roleaccounts
(for i in `egrep -h "^postmaster@" virtual_forwardings virtual_mailboxes | cut -f1`; do echo -e "$i\tOK"; done) > roleaccounts.new
(for i in `egrep -h "^abuse@" virtual_forwardings virtual_mailboxes | cut -f1`; do echo -e "$i\tOK"; done) >> roleaccounts.new
diff -Bu roleaccounts roleaccounts.new ||
if [ -s "roleaccounts.new" ]; then
	echo >> roleaccounts.new
	mv roleaccounts roleaccounts.old
	mv roleaccounts.new roleaccounts
	postmap roleaccounts
fi
rm -f roleaccounts.new

