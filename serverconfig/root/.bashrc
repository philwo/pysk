# Check for an interactive session
[ -z "$PS1" ] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

alias ll="ls -l --color=auto"
alias makepasswd="tr -cd '[:alnum:]' < /dev/urandom | head -c 12"
alias maillog="cat  /var/log/mail.log | fgrep -v 'connect from localhost.localdomain[127.0.0.1]' | fgrep -v 'disconnect from localhost.localdomain[127.0.0.1]' | fgrep -v 'dovecot: imap-login: Aborted login (no auth attempts): rip=127.0.0.1, lip=127.0.0.1, secured'"
alias mailtail="tail -f /var/log/mail.log | fgrep -v 'connect from localhost.localdomain[127.0.0.1]' | fgrep -v 'disconnect from localhost.localdomain[127.0.0.1]' | fgrep -v 'dovecot: imap-login: Aborted login (no auth attempts): rip=127.0.0.1, lip=127.0.0.1, secured'"

export PGHOST="localhost"
export PGUSER="postgres"

