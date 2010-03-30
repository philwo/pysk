#!/bin/bash

set -e
set -u

backup_root="/root/backup/psql"

mkdir -p ${backup_root}/

databases=`psql -lAt | fgrep "|" | cut -d"|" -f1 | fgrep -v "template0"`
for db in $databases; do
    
    # Dump individual tables
    #tables=`mysql -Bse 'show tables' ${db}`
    #for table in $tables; do
    #   mkdir mkdir -p ${backup_root}/${db}/
    #   file="${backup_root}/${db}/${table}.sql.xz"
    #   mysqldump --add-drop-table --allow-keywords 
    #done
    
    echo "Dumping ${db} ..."
    pg_dump -h localhost -U postgres -Fc -Z9 -bcC -f ${backup_root}/${db}.dump ${db}
done

