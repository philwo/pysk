#!/bin/bash
ssh root@haruhi "cd /opt/pysk && hg pull -u"
ssh root@mikuru "cd /opt/pysk && hg pull -u"
ssh root@yuki "cd /opt/pysk && hg pull -u"
ssh root@kyon "cd /opt/pysk && hg pull -u"
cd ~/src/pysk && hg pull -u

