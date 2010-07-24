#!/bin/bash

set -e
set -u

backup_root="/root/backup/mysql"

mkdir -p ${backup_root}/
rm -f ${backup_root}/*

databases=`mysql -Bse 'show databases' | fgrep -v "information_schema"`
for db in $databases; do
    
    # Dump individual tables
    #tables=`mysql -Bse 'show tables' ${db}`
    #for table in $tables; do
    #   mkdir mkdir -p ${backup_root}/${db}/
    #   file="${backup_root}/${db}/${table}.sql.xz"
    #   mysqldump --add-drop-table --allow-keywords 
    #done
    
    echo "Dumping ${db} ..."
    #mysqldump --add-drop-database --lock-all-tables --events --routines --triggers --allow-keywords ${db} | xz -7 > ${backup_root}/${db}.sql.xz
    mysqldump --add-drop-database --lock-all-tables --events --routines --triggers --allow-keywords ${db} | gzip -9 > ${backup_root}/${db}.sql.gz
done

