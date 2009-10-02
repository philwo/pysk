#!/bin/bash

diff -ur -x php-fpm.conf /opt/pysk/serverconfig/ / | grep -v "Only in /" | less

