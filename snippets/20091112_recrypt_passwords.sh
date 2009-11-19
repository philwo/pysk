#!/bin/bash

python /opt/pysk/pysk/manage.py shell_plus <<'EOF'
for c in Customer.objects.all():
    print "%s = %s" % (c.user.username, c.unixpw)
    c.user.set_password(c.unixpw)
    c.user.save()

exit()
EOF

