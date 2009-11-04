#!/bin/bash

set -e
set -u

cat >> /etc/sysctl.conf <<'EOF'
# Prevent "kernel NULL pointer dereference" exploits
vm.mmap_min_addr = 4096
EOF
sysctl -p

