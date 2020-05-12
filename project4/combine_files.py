#!/usr/bin/env python

#Usage: python2.7 view_pcaps.py

from sys import argv
import syslog
import time
import os

def read_other_file(other_file):
    f = open(other_file,"r")
    for line in f:
        fields = line.split('|')
        emptyfirst = fields[0]
        srcip = fields[1]
        srcport = fields[2]
        dstip = fields[3]
        dstport = fields[4]
        conntype = fields[5]

        entry = str('|%s|%s|%s|%s' % (srcip, srcport, dstip, dstport))
        #print(entry)
        #print(conntype)
        if not total_pkts.has_key(entry): 
		total_pkts[entry]=conntype
        
    f.close()

if __name__ == "__main__":
    total_pkts = {}
    read_other_file(str("cnc.txt"))
    read_other_file(str("infection.txt"))
    read_other_file(str("connections.txt"))

    for entry in total_pkts:
	print (entry + '|' + total_pkts[entry] + '|')



