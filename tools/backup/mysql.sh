#!/bin/bash
# -*- coding: utf-8 -*-

# Copyright 2006 - 2012 Philipp Wollermann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e
set -u

backup_root="/root/backup/mysql"

mkdir -p ${backup_root}/
rm -rf ${backup_root}/*

echo "Dumping users ..."
mysql -BNe "select concat('\'',user,'\'@\'',host,'\'') from mysql.user" | while read uh; do mysql -BNe "show grants for $uh" | sed 's/$/;/; s/\\\\/\\/g'; done > ${backup_root}/grants.sql

databases=`mysql -Bse 'show databases' | fgrep -v "information_schema" | fgrep -v "performance_schema"`
for db in $databases; do
    echo "Dumping ${db} ..."
    mysqldump --add-drop-database --allow-keywords -ERx --triggers ${db} | gzip -9 > ${backup_root}/${db}.sql.gz

    # Dump individual tables
    mkdir ${backup_root}/${db}
    tables=`mysql -Bse 'show tables' ${db}`
    for table in $tables; do
        echo "Dumping ${db}.${table} ..."
        mysqldump --add-drop-table --allow-keywords -ERx --triggers ${db} ${table} | gzip -9 > ${backup_root}/${db}/{$table}.sql.gz
    done
done
