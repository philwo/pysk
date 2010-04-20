#!/bin/bash

./se.sh "cd /opt/pysk/pysk && /usr/bin/python manage.py sqldiff vps | /bin/bash -l psql pysk && monit restart pysk"

