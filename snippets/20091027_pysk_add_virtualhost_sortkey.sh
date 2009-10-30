#!/bin/bash

set -e
set -u

cd /opt/pysk/pysk
echo 'ALTER TABLE "vps_virtualhost" ADD "sortkey" varchar(255);' | psql pysk
echo 'for vh in VirtualHost.objects.all(): vh.save()' | python manage.py shell_plus

