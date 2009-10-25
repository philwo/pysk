#!/bin/bash

set -e
set -u

[ ! -e /opt/ZendFramework ] && svn co http://framework.zend.com/svn/framework/standard/tags/release-1.9.3PL1 /opt/ZendFramework

