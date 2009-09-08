# Check for an interactive session
[ -z "$PS1" ] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

alias ll="ls -l --color=auto"
alias makepasswd="tr -cd '[:alnum:]' < /dev/urandom | head -c 12"

export PGHOST="localhost"
export PGUSER="postgres"

