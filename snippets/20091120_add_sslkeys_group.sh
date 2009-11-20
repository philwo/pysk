#!/bin/bash

set -e
set -u

groupadd -g 201 sslkeys
chmod 0660 /etc/ssl/private/*
chown root:sslkeys /etc/ssl/private/*
usermod -a -G sslkeys mysql

