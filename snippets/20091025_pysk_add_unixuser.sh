#!/bin/bash

groupadd -g 200 -r pysk
useradd -d /opt/pysk -g 200 -M -N -r -s /bin/false -u 200 pysk

