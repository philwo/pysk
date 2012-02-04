#/bin/bash

set -e
set -u

#echo "du -hs ." | lftp -u XXXXX,XXXXXXXX 88.198.42.117
echo "du" | lftp -u XXXXX,XXXXXXXX 88.198.42.117 | awk -v LIMIT=100 '$2=="." {print ((LIMIT*1024*1024)-$1)/1024 " MiB backup space remaining"}'
#ncftp -u XXXXX -p XXXXXXXX 88.198.42.117

