#!/bin/bash
ssh root@haruhi "cd /opt/pysk && hg st"
ssh root@mikuru "cd /opt/pysk && hg st"
ssh root@yuki "cd /opt/pysk && hg st"
ssh root@kyon "cd /opt/pysk && hg st"
cd ~/src/pysk && hg st

