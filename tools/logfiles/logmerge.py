#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
