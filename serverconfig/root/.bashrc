# Check for an interactive session
[ -z "$PS1" ] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

alias ll="ls -l --color=auto"

export PGHOST="localhost"
export PGUSER="postgres"

