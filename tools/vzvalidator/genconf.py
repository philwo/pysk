#!/usr/bin/python

import sys, os
import csv

reader = csv.reader(open("config.csv"), delimiter=",", quotechar='"')
configs = ("M", "L", "XL", "XXL")

output = {}

for row in reader:
    column = row[0]
    i = 1
    for config in configs:
        if not config in output:
            output[config] = {}
        barrier = row[i]
        limit = row[i+1]
        output[config][column] = "%s:%s" % (barrier, limit)
        i += 2

print output

for cname, columns in output.iteritems():
    print "VZ config ", cname
    #for name, value in columns.iteritems():
    #    print "%s=%s" % (name, value,)
    print

