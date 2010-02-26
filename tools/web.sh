#!/bin/bash

set -e
set -u

echo "Verschiedenes ..."
/opt/pysk/tools/passwd/passwd.py
/opt/pysk/tools/passwd/pysk_secret.sh
echo

echo "Fertig!"
