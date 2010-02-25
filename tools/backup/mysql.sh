#!/bin/bash

set -e
set -u

backup_root="/var/backup/mysql"
date=`date +%Y%m%d`

mkdir -p ${backup_root}/${date}/

databases=`mysql -Bse 'show databases' | fgrep -v "information_schema"`
for db in $databases; do
    
    # Dump individual tables
    #tables=`mysql -Bse 'show tables' ${db}`
    #for table in $tables; do
    #   mkdir mkdir -p ${backup_root}/${date}/${db}/
    #   file="${backup_root}/${date}/${db}/${table}.sql.xz"
    #   mysqldump --add-drop-table --allow-keywords 
    #done
    
    echo "Dumping ${db} ..."
    #mysqldump --add-drop-database --lock-all-tables --events --routines --triggers --allow-keywords ${db} | xz -7 > ${backup_root}/${date}/${db}.sql.xz
    mysqldump --add-drop-database --lock-all-tables --events --routines --triggers --allow-keywords ${db} | bzip2 -9 > ${backup_root}/${date}/${db}.sql.bz2
done

oldbackups=`ls -1rd ${backup_root}/???????? | sed 1,2d`
for oldbackup in $oldbackups; do
    rm -r $oldbackups
done

