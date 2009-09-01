#!/usr/bin/python

from __future__ import division, with_statement

import re
import cStringIO,operator
from os.path import basename, dirname
from glob import glob

### TABLE INDENTION

def indent(rows, hasHeader=False, headerChar='-', delim=' | ', justify='left',
           separateRows=False, prefix='', postfix='', wrapfunc=lambda x:x):
    """Indents a table by column.
       - rows: A sequence of sequences of items, one sequence per row.
       - hasHeader: True if the first row consists of the columns' names.
       - headerChar: Character to be used for the row separator line
         (if hasHeader==True or separateRows==True).
       - delim: The column delimiter.
       - justify: Determines how are data justified in their column. 
         Valid values are 'left','right' and 'center'.
       - separateRows: True if rows are to be separated by a line
         of 'headerChar's.
       - prefix: A string prepended to each printed row.
       - postfix: A string appended to each printed row.
       - wrapfunc: A function f(text) for wrapping text; each element in
         the table is first wrapped by this function."""
    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(row):
        newRows = [wrapfunc(item).split('\n') for item in row]
        return [[substr or '' for substr in item] for item in map(None,*newRows)]
    # break each logical row into one or more physical ones
    logicalRows = [rowWrapper(row) for row in rows]
    # columns of physical rows
    columns = map(None,*reduce(operator.add,logicalRows))
    # get the maximum of each column by the string length of its items
    maxWidths = [max([len(str(item)) for item in column]) for column in columns]
    rowSeparator = headerChar * (len(prefix) + len(postfix) + sum(maxWidths) + \
                                 len(delim)*(len(maxWidths)-1))
    # select the appropriate justify method
    justify = {'center':str.center, 'right':str.rjust, 'left':str.ljust}[justify.lower()]
    output=cStringIO.StringIO()
    if separateRows: print >> output, rowSeparator
    for physicalRows in logicalRows:
        for row in physicalRows:
            print >> output, \
                prefix \
                + delim.join([justify(str(item),width) for (item,width) in zip(row,maxWidths)]) \
                + postfix
        if separateRows or hasHeader: print >> output, rowSeparator; hasHeader=False
    return output.getvalue()

# written by Mike Brown
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
def wrap_onspace(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line[line.rfind('\n')+1:])
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

import re
def wrap_onspace_strict(text, width):
    """Similar to wrap_onspace, but enforces the width constraint:
       words longer than width are split."""
    wordRegex = re.compile(r'\S{'+str(width)+r',}')
    return wrap_onspace(wordRegex.sub(lambda m: wrap_always(m.group(),width),text),width)

import math
def wrap_always(text, width):
    """A simple word-wrap function that wraps text on exactly width characters.
       It doesn't split the text in words."""
    return '\n'.join([ text[width*i:width*(i+1)] \
                       for i in xrange(int(math.ceil(1.*len(text)/width))) ])
    
### MAIN

def update_ubc(global_ubc, ubc, name, column, value):
    # Initialize data structures
    if not name in global_ubc:
        global_ubc[name] = {}
    if not column in global_ubc[name]:
        global_ubc[name][column] = 0
    if not name in ubc:
        ubc[name] = {}
    
    # Increment counters
    global_ubc[name][column] += value
    ubc[name][column] = value
    
    # Special counters
    if name == "tcpsndbuf" or name == "tcprcvbuf" or name == "othersockbuf" or name == "dgramrcvbuf":
        if not "allsockbuf" in ubc:
            ubc["allsockbuf"] = {}
        if not "allsockbuf" in global_ubc:
            global_ubc["allsockbuf"] = {}
        if not column in global_ubc["allsockbuf"]:
            global_ubc["allsockbuf"][column] = 0

        ubc["allsockbuf"][column] = value
        global_ubc["allsockbuf"][column] += value
    
    return value

def check_cond(cond, errorstring, recommendation=None):
    if not cond:
        print "FAILED: ", errorstring
        if recommendation:
            print "Recommendation: ", recommendation
    return cond

regex = re.compile(r"^\s+(?P<name>\w+)\s+(?P<held>\d+)\s+(?P<maxheld>\d+)\s+(?P<barrier>\d+)\s+(?P<limit>\d+)\s+(?P<failcnt>\d+)$")
labels = ("VZID", "Name", "Held", "Held (percent)", "Max held", "Max held (percent)", "Barrier", "Limit", "Fail count")
global_ubc = {}
MAX_ULONG = 2147483647
#MAX_ULONG = 9223372036854775807
AVNUMPROC = 50
RAMSIZE = 3974 * 1024 * 1024
SWAPSIZE = 7948 * 1024 * 1024

for bc in glob("/proc/bc/*/resources"):
    if bc == "/proc/bc/0/resources": continue
    vzid = int(basename(dirname(bc)))
    rows = []
    ubc = {}
    
    bcfile = open(bc, "r")
    for line in bcfile:
        matches = regex.match(line)
        name = matches.group("name")
        
        held = update_ubc(global_ubc, ubc, name, "held", int(matches.group("held")))
        maxheld = update_ubc(global_ubc, ubc, name, "maxheld", int(matches.group("maxheld")))
        barrier = update_ubc(global_ubc, ubc, name, "barrier", int(matches.group("barrier")))
        limit = update_ubc(global_ubc, ubc, name, "limit", int(matches.group("limit")))
        failcnt = update_ubc(global_ubc, ubc, name, "failcnt", int(matches.group("failcnt")))
    
        percent_held = 0
        percent_maxheld = 0
        if barrier > 0:
            percent_held = held / barrier * 100
            percent_maxheld = maxheld / barrier * 100
        
        rows.append("%s;%s;%s;= %.2f%%;%s;= %.2f%%;%s;%s;%s" % (vzid, name, held, percent_held, maxheld, percent_maxheld, barrier, limit, failcnt))
    bcfile.close()

    print
    print vzid
    #table_rows = sorted([row.split(";") for row in rows], key=lambda x: float(x[2].strip("= %")), reverse=True)
    table_rows = [row.split(";") for row in rows]
    print indent([labels] + table_rows, hasHeader=True)
    
    # Barrier should be less or equal than limit
    for name, bc in ubc.iteritems():
        check_cond(bc["barrier"] <= bc["limit"],
            "%s: Barrier should be less or equal than limit" % (name,))
    
    # numproc
    check_cond(ubc["numproc"]["barrier"] == ubc["numproc"]["limit"],
        "numproc barrier should be set to limit")
    check_cond(ubc["numproc"]["barrier"] >= AVNUMPROC*2,
        "numproc too small for estimated number of processes")
    
    # numtcpsock
    check_cond(ubc["numtcpsock"]["barrier"] == ubc["numtcpsock"]["limit"],
        "numtcpsock barrier should be set to limit")
    
    # numothersock
    check_cond(ubc["numothersock"]["barrier"] == ubc["numothersock"]["limit"],
        "numothersock barrier should be set to limit")
    
    # vmguarpages
    check_cond(ubc["vmguarpages"]["limit"] == MAX_ULONG,
        "vmguarpages::limit should be set to MAX_ULONG")
    
    # kmemsize
    # kmemsize should be enough for the expected number of processes
    check_cond(ubc["kmemsize"]["barrier"] >= 40 * 1024 * AVNUMPROC + ubc["dcachesize"]["limit"], 
        "kmemsize should be enough for the expected number of processes")
    # It is important to have a certain safety gap between the barrier and the limit of the kmemsize parameter
    check_cond(ubc["kmemsize"]["limit"] >= int(ubc["kmemsize"]["barrier"] * 1.10),
        "It is important to have a certain safety gap (10%) between the barrier and the limit of the kmemsize parameter")

    ### tcpsndbuf / tcprcvbuf / othersockbuf / dgramrcvbuf
    # Send buffers should have enough space for all sockets
    check_cond(ubc["tcpsndbuf"]["limit"] - ubc["tcpsndbuf"]["barrier"] >= 2.5 * 1024 * ubc["numtcpsock"]["limit"],
        "TCP Send buffers should have enough space for all sockets")

    check_cond(ubc["othersockbuf"]["limit"] - ubc["othersockbuf"]["barrier"] >= 2.5 * 1024 * ubc["numothersock"]["limit"],
        "OtherSOck Send buffers should have enough space for all sockets")

    # Other TCP socket buffers should be big enough
    check_cond(ubc["tcprcvbuf"]["limit"] - ubc["tcprcvbuf"]["barrier"] >= 2.5 * 1024 * ubc["numtcpsock"]["limit"],
        "Other TCP socket buffers should be big enough")

    check_cond(ubc["tcprcvbuf"]["barrier"] >= 64 * 1024,
        "Other TCP socket buffers should be big enough")

    check_cond(ubc["tcpsndbuf"]["barrier"] >= 64 * 1024,
        "Other TCP socket buffers should be big enough")

    # UDP socket buffers should be large enough if the system is not tight on memory
    check_cond(ubc["dgramrcvbuf"]["barrier"] >= 129 * 1024,
        "UDP socket buffers should be large enough if the system is not tight on memory")
    check_cond(ubc["othersockbuf"]["barrier"] >= 129 * 1024,
        "OtherSock socket buffers should be large enough if the system is not tight on memory")
    
    # oomguarpages
    check_cond(ubc["oomguarpages"]["limit"] == MAX_ULONG,
        "The meaning of the limit for the oomguarpages parameter is unspecified in the current version.")
    if ubc["privvmpages"]["limit"] <= ubc["oomguarpages"]["barrier"]:
        print "privvmpages <= oomguarpages: Significantly reduced chance of getting killed in OOM situation"
    if ubc["privvmpages"]["limit"] <= ubc["oomguarpages"]["barrier"] // 2:
        print "privvmpages <= oomguarpages / 2: Guaranteed to not getting killed in OOM situation"
        
    # privvmpages
    check_cond(ubc["privvmpages"]["limit"] >= int(ubc["privvmpages"]["barrier"] * 1.10),
        "There should be a safety gap (10%) between the barrier and the limit for privvmpages!")
    check_cond(ubc["privvmpages"]["barrier"] >= ubc["vmguarpages"]["barrier"], 
        "Memory allocation limits should not be less than the guarantee")
    check_cond(ubc["privvmpages"]["limit"] * 4096 <= 0.6 * RAMSIZE,
        "privvmpages too high: Container may easily cause an excessive swap-out and very bad performance of the whole system!",
        "Set privvmpages to max %.0f" % (0.6 * RAMSIZE / 4096,))
    
    # lockedpages
    check_cond(ubc["lockedpages"]["limit"] == ubc["lockedpages"]["barrier"],
        "lockedpages limit should be set to barrier")
    check_cond(ubc["lockedpages"]["limit"] >= 512,
        "lockedpages limit should be at least 512 pages")
    
    # shmpages
    check_cond(ubc["shmpages"]["limit"] == ubc["shmpages"]["barrier"],
        "shmpages limit should be set to barrier")
    
    # physpages
    check_cond(ubc["physpages"]["barrier"] == 0,
        "physpages barrier should be set to 0")
    check_cond(ubc["physpages"]["limit"] == MAX_ULONG,
        "physpages limit should be set to MAX_ULONG")
    
    # numfile
    check_cond(ubc["numfile"]["limit"] == ubc["numfile"]["barrier"],
        "numfile limit should be set to barrier")
    check_cond(ubc["numfile"]["limit"] >= AVNUMPROC * 32,
        "Number of files limit should be adequate for the expected number of processes")
    
    # numflock
    check_cond(ubc["numflock"]["limit"] >= int(ubc["numflock"]["barrier"] * 1.10),
        "numflock should have a gap (10%) between the barrier and the limit")
    
    # numpty
    check_cond(ubc["numpty"]["limit"] == ubc["numpty"]["barrier"],
        "numpty barrier should be set equal to the limit")
    
    # numsiginfo
    check_cond(ubc["numsiginfo"]["limit"] == ubc["numsiginfo"]["barrier"],
        "numsiginfo barrier should be set equal to the limit")
    check_cond(ubc["numsiginfo"]["limit"] <= 1024,
        "numsiginfo: It is unlikely that any container will need the limit greater than the Linux default - 1024")

    # dcachesize
    check_cond(ubc["dcachesize"]["barrier"] >= ubc["numfile"]["limit"] * 384,
        "The limit on the total size of dentry and inode structures locked in memory should be adequate for allowed number of files",
        "Set dcachesize::barrier to %s" % (ubc["numfile"]["limit"] * 384,))
    check_cond(ubc["dcachesize"]["limit"] >= int(ubc["dcachesize"]["barrier"] * 1.10),
        "dcachesize should have a gap (10%) between the barrier and the limit")
    
    # numiptent
    check_cond(ubc["numiptent"]["limit"] == ubc["numiptent"]["barrier"],
        "numiptent barrier should be set equal to the limit")
    check_cond(ubc["numiptent"]["limit"] >= 100 and ubc["numiptent"]["limit"] <= 200,
        "numiptent should be between 100 and 200")

print
print "Validating systemwide configuration"

print
print "Low memory (x86 specific):"
utilization = (global_ubc["kmemsize"]["held"] + global_ubc["allsockbuf"]["held"]) / (0.4 * min(RAMSIZE, 832 * 1024 * 1024))
commitment  = (global_ubc["kmemsize"]["limit"] + global_ubc["allsockbuf"]["limit"]) / (0.4 * min(RAMSIZE, 832 * 1024 * 1024))
print "-> Utilization: %.2f" % (utilization,)
print "-> Commitment level (0.8 - 1.2): %.2f" % (commitment,)

print
print "Total RAM"
utilization = (global_ubc["physpages"]["held"] * 4096 + global_ubc["kmemsize"]["held"] + global_ubc["allsockbuf"]["held"]) / RAMSIZE
print "-> Utilization (0.8 - 1.0): %.2f" % (utilization,)
#print "-> Commitment level: %.2f" % (commitment,)

print
print "Memory and swap space"
utilization = (global_ubc["oomguarpages"]["held"] * 4096 + global_ubc["kmemsize"]["held"] + global_ubc["allsockbuf"]["held"]) / (RAMSIZE + SWAPSIZE)
util_lowbound = RAMSIZE / (RAMSIZE + SWAPSIZE)
util_highbound = (RAMSIZE + 0.5 * SWAPSIZE) / (RAMSIZE + SWAPSIZE)
commitment = (global_ubc["oomguarpages"]["barrier"] * 4096 + global_ubc["kmemsize"]["limit"] + global_ubc["allsockbuf"]["limit"]) / (RAMSIZE + SWAPSIZE)
print "-> Utilization: %.2f [lowmark: %.2f   highmark: %.2f]" % (utilization, util_lowbound, util_highbound)
print "-> Commitment level (0.8 - 1.0): %.2f" % (commitment,)

print
print "Allocated memory"
utilization = (global_ubc["privvmpages"]["held"] * 4096 + global_ubc["kmemsize"]["held"] + global_ubc["allsockbuf"]["held"]) / (RAMSIZE + SWAPSIZE)
commitment = (global_ubc["vmguarpages"]["barrier"] * 4096 + global_ubc["kmemsize"]["limit"] + global_ubc["allsockbuf"]["limit"]) / (RAMSIZE + SWAPSIZE)
commitment2 = (global_ubc["privvmpages"]["limit"] * 4096 + global_ubc["kmemsize"]["limit"] + global_ubc["allsockbuf"]["limit"]) / (RAMSIZE + SWAPSIZE)
print "-> Utilization: %.2f" % (utilization,)
print "-> Commitment level (< 1.0): %.2f" % (commitment,)
print "-> Second commitment level (1.5 - 4.0): %.2f" % (commitment2,)

print "Finished."
