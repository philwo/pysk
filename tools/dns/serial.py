#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright 2006 - 2012 Philipp Wollermann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import os.path
import optparse
import cPickle as pickle
from datetime import date
from glob import glob
import hashlib


def update(opts, zones):
    t = date.today().strftime("%Y%m%d")

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

            if opts.verbose:
                print >>sys.stderr, "%s: Hash mismatch, updated serial from %s to %s" % (zonename, oldserial, zones[zonename]["serial"],)

    pickle.dump(zones, open("/var/named/serial", "w"))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    zones = {}
    if os.path.exists("/var/named/serial"):
        zones = pickle.load(open("/var/named/serial", "r"))

    usage = "usage: %s [--update] [zone]" % (argv[0])
    parser = optparse.OptionParser(usage)
    parser.add_option("-u", "--update", action="store_true", dest="update", default=False)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")
    (opts, args) = parser.parse_args(argv[1:])

    if opts.update:
        update(opts, zones)

    assert(len(args) <= 1)
    if len(args) == 1:
        if args[0] in zones:
            print zones[args[0]]["serial"]
        else:
            print >>sys.stderr, "Zone not found!"
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
