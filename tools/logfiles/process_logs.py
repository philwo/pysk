#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import with_statement

import apachelog
import sys
import os
import os.path
import psycopg2
import psycopg2.extras
import threading
import Queue
import socket
from datetime import datetime
import time
from socket import inet_pton, gethostbyaddr, AF_INET, AF_INET6
from tempfile import NamedTemporaryFile, mkstemp
from subprocess import Popen, PIPE, call
from optparse import OptionParser
from glob import glob


class ResolveThread(threading.Thread):
    def __init__(self, inputQueue, outputDict, exitEvent):
        threading.Thread.__init__(self)
        self.inputQueue = inputQueue
        self.outputDict = outputDict
        self.exitEvent = exitEvent

    def run(self):
        while True:
            try:
                i = self.inputQueue.get(True, 1)

                # Check if input is valid IPv4 or IPv6
                valid_input = False
                try:
                    inet_pton(AF_INET, i)
                    valid_input = True
                except socket.error:
                    try:
                        inet_pton(AF_INET6, i)
                        valid_input = True
                    except socket.error:
                        pass

                if valid_input:
                    # Try to resolve IP to hostname
                    try:
                        rdns = gethostbyaddr(i)[0]
                    except socket.herror:
                        # If we can't resolve it, store the IP
                        rdns = i
                    self.outputDict[i] = rdns
            except Queue.Empty:
                if self.exitEvent.isSet():
                    break
                pass


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = OptionParser()
    parser.add_option("-v", "--vhost", dest="vhostoverride", help="if logfile doesn't include vhost column, override it with this", metavar="VHOST")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Turn on debugging output", default=False)
    (options, args) = parser.parse_args(argv)

    if options.debug:
        print >> sys.stderr, "Debug mode activated"

    OUTPUTDIR = "/opt/pysk/wwwlogs"

    # Get list of vhosts
    db = psycopg2.connect("host='localhost' user='pysk' password='XXXXXXXXXXXXXXX' dbname='pysk'")
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT trim(both '.' from vh.name || '.' || d.name) as vhost FROM vps_virtualhost vh, vps_domain d WHERE vh.domain_id = d.id ORDER BY vhost"
    cursor.execute(query)
    rows = cursor.fetchall()

    vhosts = {}
    for row in rows:
        vhosts[row["vhost"]] = {"logfile": None}

    # RDNS
    exitEvent = threading.Event()
    inputQueue = Queue.Queue()
    resolvedIPDict = {}
    outputDict = {}
    workers = [ResolveThread(inputQueue, outputDict, exitEvent) for i in range(0, 100)]
    for worker in workers:
        worker.start()

    # Log formats
    p_igowo = apachelog.parser(apachelog.formats["igowo"])
    p_vhextendedio = apachelog.parser(apachelog.formats["vhextendedio"])
    p_vhextended = apachelog.parser(apachelog.formats["vhextended"])
    p_extended = apachelog.parser(apachelog.formats["extended"])

    for fname in glob(os.path.join(OUTPUTDIR, "inbox") + "/*"):
        fname = os.path.realpath(fname)
        print "Processing %s ..." % (fname,)
        with open(fname, "rb") as f:
            for line in f:
                # Try to parse line
                try:
                    try:
                        data = p_igowo.parse(line)
                    except apachelog.ApacheLogParserError:
                        try:
                            data = p_vhextendedio.parse(line)
                        except apachelog.ApacheLogParserError:
                                try:
                                    data = p_vhextended.parse(line)
                                except apachelog.ApacheLogParserError:
                                    if options.vhostoverride:
                                        data = p_extended.parse(line)
                                        data["%v"] = options.vhostoverride
                                    else:
                                        raise

                    if cursor != None:
                        vhost = data["%v"]

                        if not vhost in vhosts:
                            continue

                        # Create a new logfile if we don't already have done so
                        if vhosts[vhost]["logfile"] is None:
                            vhosts[vhost]["logfile"] = NamedTemporaryFile(prefix=vhost, dir=os.path.join(OUTPUTDIR, "temp"))
                        logfile = vhosts[vhost]["logfile"]

                        #if "%A" in data:
                        #    local_ip = data["%A"]
                        #else:
                        #    local_ip = ""

                        if "%D" in data:
                            utime = data["%D"]
                            # stored in milliseconds instead of microseconds?
                            if '.' in utime:
                                utime = int(float(utime) * 1000)
                        else:
                            utime = None
                        r_host = data["%h"]

                        # Resolve the host, take measures to not resolve the same IP twice
                        if not r_host in resolvedIPDict:
                            resolvedIPDict[r_host] = True
                            inputQueue.put(r_host)

                        #r_logname = data["%l"]
                        r_user = data["%u"]
                        req_dt = apachelog.parse_date(data["%t"])

                        request = data["%r"]
                        status = int(data["%>s"])

                        if data["%b"] != "-":
                            response_size = int(data["%b"])
                        else:
                            response_size = 0

                        referer = data["%{Referer}i"]
                        user_agent = data["%{User-Agent}i"]

                        if "%I" in data:
                            bytes_recv = int(data["%I"])
                        else:
                            bytes_recv = None

                        if "%O" in data:
                            bytes_sent = int(data["%O"])
                        else:
                            bytes_sent = None

                        # Build logline
                        logline = u'%010d %s - %s [%s +0000] "%s" %s %s "%s" "%s"' % (time.mktime(req_dt.timetuple()), r_host, r_user, req_dt.strftime("%d/%b/%Y:%H:%M:%S"), request, status, response_size, referer, user_agent)
                        # If input/output bytes available, append them
                        if bytes_recv and bytes_sent:
                            logline += " %s %s" % (bytes_recv, bytes_sent,)

                        logfile.write(logline.encode("utf-8") + "\n")
                except UnicodeDecodeError:
                    if options.debug:
                        print >> sys.stderr, "UnicodeDecodeError on line %s" % line
                except apachelog.ApacheLogParserError:
                    if options.debug:
                        print >> sys.stderr, "ApacheLogParserError on line %s" % line
                except:
                    sys.stderr.write("Unable to parse %s" % line)
                    raise
        # Delete the processed logfile from the inbox
        os.unlink(fname)

    # Sort logfiles by date, strip timestamp field
    for (vhname, vh) in vhosts.iteritems():
        if not vh["logfile"] is None:
            print "Sorting %s ..." % (vh["logfile"].name,)
            # Create output logfile
            (sorted_logfile_handle, sorted_logfile_name) = mkstemp(prefix=vhname, dir=os.path.join(OUTPUTDIR, "temp"))
            sorted_logfile = os.fdopen(sorted_logfile_handle, "w+b")

            # Process input -> output
            p1 = Popen(["sort", "-n", vh["logfile"].name], stdout=PIPE)
            p2 = Popen(["cut", "-d ", "-f2-"], stdin=p1.stdout, stdout=sorted_logfile)
            p1.wait()
            p2.wait()

            # Close input (deletes the file)
            vh["logfile"].close()

            # Close output and atomically move it into the "pending" directory for further processing
            sorted_logfile.close()
            pending_dir = os.path.join(OUTPUTDIR, "pending", vhname)
            if not os.path.exists(pending_dir):
                os.makedirs(pending_dir)
            timestamp = int(time.mktime(datetime.now().timetuple()))
            os.rename(sorted_logfile_name, os.path.join(pending_dir, str(timestamp) + ".log"))

    # Wait until all rdns workers are finished
    exitEvent.set()
    for worker in workers:
        worker.join()

    # Generate DNS cache
    if len(outputDict) > 0:
        with open(os.path.join(OUTPUTDIR, "dnscache.txt"), "w+b") as f:
            for (ip, rdns) in outputDict.iteritems():
                f.write("%s %s\n" % (ip, rdns))

    # Delete old config files
    for f in glob("/etc/awstats/awstats.*.conf"):
        os.unlink(f)

    # Generate new config files
    for (vhname, vh) in vhosts.iteritems():
            conffile = "/etc/awstats/awstats.%s.conf" % vhname
            with open(conffile + ".new", "w") as f:
                logfilesdir = os.path.join(OUTPUTDIR, "pending", vhname, "*.log")
                f.write('LogFile="/opt/pysk/tools/logfiles/logmerge.py %s |"\n' % logfilesdir)
                f.write('SiteDomain="%s"\n' % vhname)
                f.write('HostAliases="www.%s"\n' % vhname)
                f.write('DirData="/var/lib/awstats/%s/"\n' % vhname)
                f.write('Include "/etc/awstats/awstats.conf.local"\n')
            os.rename(conffile + ".new", conffile)

    # Preprocess pending logfiles before statistics run

    ## Delete empty logfiles
    call(["/usr/bin/find", os.path.join(OUTPUTDIR, "pending"), "-name", "*.log", "-size", "0", "-delete"])

    # Run statistics

    ## Create list of vhosts which have logfiles
    vhosts_with_logs = list(set([os.path.basename(os.path.dirname(i)) for i in glob(os.path.join(OUTPUTDIR, "pending", "*", "*.log"))]))

    ## Run awstats for these vhosts
    for v in vhosts_with_logs:
        call(["/usr/local/awstats/wwwroot/cgi-bin/awstats.pl", "-config=%s" % (v,), "-showcorrupted"])

    # Finalize processed logfiles
    processed_logfiles = glob(os.path.join(OUTPUTDIR, "processed", "*", "*.log"))

    ## Compress with bzip2 -9
    for pl in processed_logfiles:
        call(["bzip2", "-9", pl])

    # Fix permissions of awstats directory
    call("chmod 0750 /var/lib/awstats", shell=True)
    call("chmod 0750 /var/lib/awstats/*", shell=True)
    call("chmod 0660 /var/lib/awstats/*/*", shell=True)
    call("chown pysk:http /var/lib/awstats", shell=True)
    call("chown pysk:http /var/lib/awstats/*", shell=True)
    call("chown pysk:http /var/lib/awstats/*/*", shell=True)
    call("find /var/lib/awstats/ -name \"*.tmp.*\" -delete", shell=True)

if __name__ == "__main__":
    sys.exit(main())
