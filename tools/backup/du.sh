#/bin/bash
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

#echo "du -hs ." | lftp -u XXXXX,XXXXXXXX 88.198.42.117
echo "du" | lftp -u XXXXX,XXXXXXXX 88.198.42.117 | awk -v LIMIT=100 '$2=="." {print ((LIMIT*1024*1024)-$1)/1024 " MiB backup space remaining"}'
#ncftp -u XXXXX -p XXXXXXXX 88.198.42.117

