#!/bin/bash

find /var/lib/awstats/ -name "*.tmp.*" -delete
rsync -av -e ssh --delete /var/lib/awstats/ root@igowo.de:/var/lib/awstats/
ssh root@igowo.de chmod 0750 /var/lib/awstats /var/lib/awstats/* /var/lib/awstats/*/*
ssh root@igowo.de chown 5000:5000 /var/lib/awstats /var/lib/awstats/* /var/lib/awstats/*/*

