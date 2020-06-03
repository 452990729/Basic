#!/usr/bin/env python

import sys
import os

root, dirs, files = next(os.walk(sys.argv[1]))
for f in files:
    print f
for d in dirs:
    print d
