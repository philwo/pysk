#!/bin/bash

set -e
set -u

cd /etc/postfix

if [ ! -e virtual_mailboxes ]; then   touch virtual_mailboxes;   postmap virtual_mailboxes; fi
if [ ! -e virtual_forwardings ]; then touch virtual_forwardings; postmap virtual_forwardings; fi
if [ ! -e virtual_domains ]; then     touch virtual_domains;     postmap virtual_domains; fi
if [ ! -e roleaccounts ]; then        touch roleaccounts;        postmap roleaccounts; fi

rm -f virtual_mailboxes.new virtual_forwardings.new virtual_domains.new
touch virtual_mailboxes.new virtual_forwardings.new virtual_domains.new

postfix set-permissions 2>/dev/null || /bin/true

# virtual_mailboxes
QUERY="SELECT m.mail || '@' || d.name AS mail, d.name || '/' || m.mail || '/Maildir/' FROM vps_mailbox m, vps_domain d WHERE m.active = true AND m.domain_id = d.id"
psql -At -F $'\t' -U postgres -h localhost -c"$QUERY" pysk | sort > virtual_mailboxes.new

# virtual_domains
QUERY="(SELECT DISTINCT d.name AS domain, 'dummy' AS target FROM vps_mailbox m, vps_domain d WHERE m.active = true AND m.domain_id = d.id ORDER BY d.name) UNION (SELECT DISTINCT d.name AS domain, 'dummy' AS target FROM vps_forwarding f, vps_domain d WHERE f.active = true AND f.domain_id = d.id ORDER BY d.name)"
psql -At -F $'\t' -U postgres -h localhost -c"$QUERY" pysk | sort > virtual_domains.new

# virtual_forwardings
QUERY="( SELECT f.source || '@' || d.name AS source, f.target FROM vps_forwarding f, vps_domain d WHERE f.active = true AND f.domain_id = d.id ) UNION ( SELECT DISTINCT 'postmaster@' || d.name AS source, 'philipp@igowo.de' AS target FROM vps_mailbox m, vps_domain d WHERE m.domain_id = d.id ) UNION ( SELECT DISTINCT 'postmaster@' || d.name AS source, 'philipp@igowo.de' AS target FROM vps_forwarding f, vps_domain d WHERE f.domain_id = d.id ) UNION ( SELECT DISTINCT 'abuse@' || d.name AS source, 'philipp@igowo.de' AS target FROM vps_mailbox m, vps_domain d WHERE m.domain_id = d.id ) UNION ( SELECT DISTINCT 'abuse@' || d.name AS source, 'philipp@igowo.de' AS target FROM vps_forwarding f, vps_domain d WHERE f.domain_id = d.id )"
psql -At -F $'\t' -U postgres -h localhost -c"$QUERY" pysk | sort -t '@' -k 2 > virtual_forwardings.new

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

