#!/usr/bin/env python2

import os
import sys


def FormatSize(byte):
    byte = float(byte)
    kb = byte / 1024
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)

def GetFileSize(path):
    size = os.path.getsize(path)
    return formatSize(size)

def 

def GetFileSize()
