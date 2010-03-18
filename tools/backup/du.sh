#/bin/bash

set -e
set -u

#echo "du -hs ." | lftp -u 48554,vzOQuQBd 88.198.42.117
echo "du" | lftp -u 48554,vzOQuQBd 88.198.42.117 | awk -v LIMIT=100 '$2=="." {print ((LIMIT*1024*1024)-$1)/1024 " MiB backup space remaining"}'
#ncftp -u 48554 -p vzOQuQBd 88.198.42.117

