#!/bin/bash

PHP_FCGI_MAX_REQUESTS=100
/usr/bin/spawn-fcgi -s /tmp/php-{{username}}.sock -M 0660 -P /var/run/php-{{username}}.pid -u {{username}} -g {{username}} -U {{username}} -G http -C {{php_instances}} /usr/bin/php-cgi
