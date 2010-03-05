#!/bin/bash

./se.sh "cd /opt/pysk && hg pull -u && hg merge ; hg commit -m'automatic commit' && hg push"

