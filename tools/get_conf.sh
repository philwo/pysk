#!/bin/bash

set -e
set -u

source /etc/confroot

# Package management
rm -f /usr/sbin/remove-orphans # <-- old version
wget -q -O/usr/local/sbin/remove-orphans $CONFROOT/remove-orphans
wget -q -O/usr/local/sbin/agi $CONFROOT/agi
wget -q -O/usr/local/sbin/agu $CONFROOT/agu
wget -q -O/usr/local/sbin/agr $CONFROOT/agr
wget -q -O/usr/local/sbin/debcommit $CONFROOT/debcommit
wget -q -O/usr/local/sbin/ps_mem.py $CONFROOT/ps_mem.py

chmod +x /usr/local/sbin/{remove-orphans,agi,agu,agr,debcommit,ps_mem.py}

# vim
wget -q -O/etc/vim/vimrc.local $CONFROOT/vimrc.local

# PHP
if [ -d "/etc/php5/cgi" ]; then
    wget -q -O/etc/php5/cgi/php.ini $CONFROOT/php.ini
fi

if [ -d "/etc/php5/cli" ]; then
    wget -q -O/etc/php5/cli/php.ini $CONFROOT/php.ini
fi

if [ -d "/etc/php5/apache2" ]; then
    wget -q -O/etc/php5/apache2/php.ini $CONFROOT/php.ini
fi

# Postfix
rm -rf /etc/postfix/sasl
wget -q -O/etc/postfix/main.cf $CONFROOT/postfix_main.cf
wget -q -O/etc/postfix/master.cf $CONFROOT/postfix_master.cf

#cat > /etc/aliases << EOF
#postmaster: philipp@igowo.de
#root: philipp@igowo.de
#$MAINUSER: $MAINEMAIL
#EOF
newaliases

# Apache
wget -q -O/etc/apache2/apache2.conf $CONFROOT/apache2.conf
> /etc/apache2/httpd.conf

# vsftpd
wget -q -O/etc/vsftpd.conf $CONFROOT/vsftpd.conf

# misc files
wget -q -O/etc/bash.bashrc $CONFROOT/bash.bashrc
wget -q -O/etc/perl/CPAN/Config.pm $CONFROOT/CPAN_Config.pm
#wget -q -O/etc/apt/listchanges.conf $CONFROOT/apt_listchanges.conf

