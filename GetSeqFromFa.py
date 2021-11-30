#!/usr/bin/env python2


import sys
import re
import argparse
from HTSeq import FastaReader

def MakeFa(file_in):
    dict_fa = {}
    for item in FastaReader(file_in):
        lb = '.'.join(re.split('\.', item.name)[:-1])
        dict_fa[lb] = str(item.seq)
    return dict_fa

def GetById(file_in, dict_fa):
    with open(file_in, 'r') as f:
        for line in f:
            ID = re.split('\t', line.strip())[0]
            print '>'+ID+'\n'+dict_fa[ID]

def main():
    dict_fa = MakeFa(sys.argv[1])
    GetById(sys.argv[2], dict_fa)


if __name__ == '__main__':
    main()
