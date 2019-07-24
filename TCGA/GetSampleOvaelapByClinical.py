#!/usr/bin/env python2


import sys
import re
import argparse
import pandas as pd

def GetClinical(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def GetClassData(file_in, pd_data):
    out = open('OverlapClinicalSample.txt', 'w')
    with open(file_in, 'r') as f:
        for line in f:
            line = line.strip()
            lb = '-'.join(re.split('-', line)[:3])
            tp = re.split('\t', line)[1]
            if lb in pd_data.index and tp == 'Cancer':
                out.write(line+'\n')
            if tp == 'Normal':
                out.write(line+'\n')
    out.close()

def main():
    parser = argparse.ArgumentParser(description="Overlap useful clinincal data by SampleClass file")
    parser.add_argument('-s', help='input usefule clinical matrix', required=True)
    parser.add_argument('-c', help='input sample class file no header', required=True)
    argv=vars(parser.parse_args())
    pd_data = GetClinical(argv['s'])
    GetClassData(argv['c'], pd_data)


if __name__ == '__main__':
    main()
