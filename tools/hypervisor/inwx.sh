#!/bin/bash

set -e
set -u

zone=$1

host ns.inwx.de
host ns2.inwx.de
host ns3.inwx.de

watch -n5 "dig @ns.inwx.de $zone SOA; dig @ns2.inwx.de $zone SOA; dig @ns3.inwx.de $zone SOA"

