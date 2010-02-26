#!/bin/bash

set -e
set -u

backup_root="/root/backup/psql"
date=`date +%Y%m%d`

mkdir -p ${backup_root}/${date}/

databases=`psql -lAt | fgrep "|" | cut -d"|" -f1 | fgrep -v "template0"`
for db in $databases; do
    
    # Dump individual tables
    #tables=`mysql -Bse 'show tables' ${db}`
    #for table in $tables; do
    #   mkdir mkdir -p ${backup_root}/${date}/${db}/
    #   file="${backup_root}/${date}/${db}/${table}.sql.xz"
    #   mysqldump --add-drop-table --allow-keywords 
    #done
    
    echo "Dumping ${db} ..."
    pg_dump -Fc -Z9 -bcC -f ${backup_root}/${date}/${db}.dump ${db}
done

oldbackups=`ls -1rd ${backup_root}/???????? | sed 1,2d`
for oldbackup in $oldbackups; do
    rm -r $oldbackups
done

