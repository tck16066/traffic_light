#!/usr/bin/python

#handles input from stdin

import sys
from select import select


read_timeout = 10

rlist, _, _ = select([sys.stdin], [], [], read_timeout)
if rlist:
    s = sys.stdin.readline()
    print s
else:
    print "No input. Moving on..."

