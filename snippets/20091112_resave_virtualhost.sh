#!/bin/bash

set -e
set -u

python /opt/pysk/pysk/manage.py shell_plus <<'EOF'
for vh in VirtualHost.objects.all():
    vh.save()

exit()
EOF

