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
