# Check for an interactive session
[ -z "$PS1" ] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

export PGHOST="yuki.igowo.de"
export PGUSER="postgres"
