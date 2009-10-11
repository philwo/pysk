#!/bin/bash
ssh root@haruhi "cd /opt/pysk && hg diff"
ssh root@mikuru "cd /opt/pysk && hg diff"
ssh root@yuki "cd /opt/pysk && hg diff"
ssh root@kyon "cd /opt/pysk && hg diff"
cd ~/src/pysk && hg diff

