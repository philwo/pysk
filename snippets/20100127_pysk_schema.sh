#!/bin/bash

set -e
set -u
set -x

psql pysk < /opt/pysk/snippets/20100127_pysk_schema.sql


