#!/bin/bash

set -e
set -u

fgrep vm.mmap_min_addr /etc/sysctl.conf >/dev/null || cat >> /etc/sysctl.conf <<'EOF'
# Prevent "kernel NULL pointer dereference" exploits
vm.mmap_min_addr = 4096
EOF
sysctl -p

