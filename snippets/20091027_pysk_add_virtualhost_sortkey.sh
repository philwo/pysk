#!/bin/bash

set -e
set -u

echo 'ALTER TABLE "vps_virtualhost" ADD "sortkey" varchar(255);' | psql pysk

python /opt/pysk/pysk/manage.py <<'EOF'
for vh in VirtualHost.objects.all():
    vh.save()

exit()
EOF

