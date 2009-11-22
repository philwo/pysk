#!/bin/bash

python /opt/pysk/pysk/manage.py shell_plus <<'EOF'
for u in User.objects.all():
    u.user_permissions.clear()
    u.user_permissions.add(*Permission.objects.all().filter(content_type__app_label="vps", content_type__model__in=["nsentry", "virtualhost", "alias", "directalias", "mailbox", "forwarding"]))
    u.save()

exit()
EOF

