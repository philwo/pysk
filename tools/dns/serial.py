#!/usr/bin/env python
# encoding: utf-8
"""
serial.py - SOA serial incrementer

Copyright (c) 2010 Philipp Wollermann. All rights reserved.
"""

import os, sys, os.path
import optparse
import cPickle as pickle
from datetime import date
from glob import glob
import hashlib
import pprint

t = date.today().strftime("%Y%m%d")

zones = {}
if os.path.exists("/var/named/serial"):
    zones = pickle.load(open("/var/named/serial", "r"))

def update(self):
for zonefile in glob("/var/named/pysk/db.*"):
    zonename = os.path.basename(zonefile)[3:]

    if not zonename in zones:
        zones[zonename] = {}
        zones[zonename]["hash"] = ""
        zones[zonename]["serial"] = 0

    newhash = hashlib.sha512("".join(open(zonefile, "r").readlines())).hexdigest()

    if newhash != zones[zonename]["hash"]:
        # Update stored hash of zonefile
        zones[zonename]["hash"] = newhash
        oldserial = zones[zonename]["serial"]

        # Do we already have a serial?
        if zones[zonename]["serial"] == 0:
            # No
            c = 1
        else:
            # Yes, but is it from today?
            d = str(zones[zonename]["serial"])[:8]
            if (t != d):
                # No
                c = 1
            else:
                # Yes
                c = int(str(zones[zonename]["serial"])[8:]) + 1
        zones[zonename]["serial"] = "%s%02i" % (t, c)
        print >>sys.stderr, "%s: Hash mismatch, updated serial from %s to %s" % (zonename, oldserial, zones[zonename]["serial"],)

#pprint.PrettyPrinter(indent=4).pprint(zones)
pickle.dump(zones, open("/var/named/serial", "w"))

