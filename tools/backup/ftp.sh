#/bin/bash

set -e
set -u

#lftp -u 48554,vzOQuQBd 88.198.42.117
ncftp -u 48554 -p vzOQuQBd 88.198.42.117

