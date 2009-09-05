#!/bin/bash

diff -ur /opt/pysk/serverconfig/ / | grep -v "Only in /" | less

