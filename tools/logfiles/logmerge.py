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

import sys
import os
import os.path
from optparse import OptionParser
from subprocess import call


def main(argv=None):
    """
    Wrapper for logresolvemerge.pl which moves the processed logfiles away after successful processing

    """
    if argv is None:
        argv = sys.argv

    parser = OptionParser()
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Turn on debugging output", default=False)
    (options, args) = parser.parse_args(argv)
    args = args[1:]

    OUTPUTDIR = "/opt/pysk/wwwlogs"

    if options.debug:
        print >> sys.stderr, "Debug mode activated"

    ret = call(["/opt/pysk/tools/logfiles/logresolvemerge.pl"] + args)

    if ret == 0:
        #print "Moving logfiles from pending to processed ..."
        for fname in args:
            vhostname = os.path.basename(os.path.dirname(fname))
            if not os.path.exists(os.path.join(OUTPUTDIR, "processed", vhostname)):
                os.makedirs(os.path.join(OUTPUTDIR, "processed", vhostname))
            os.rename(fname, os.path.join(OUTPUTDIR, "processed", vhostname, os.path.basename(fname)))

    return ret

if __name__ == "__main__":
    sys.exit(main())
