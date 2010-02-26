#!/bin/bash

set -e
set -u

for profile in /etc/tartarus/*.conf; do
    /usr/bin/tartarus $* "$profile"
done

