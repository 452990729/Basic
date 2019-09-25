#!/usr/bin/env python2


import re
import os
import argparse
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def Trim(pd_data, outfile, row):
    list_tmp = []
    if row:
        for value in pd_data.index:
            lb = '-'.join(re.split('-', value)[:3])
            list_tmp.append(lb)
        pd_data.index = list_tmp
        pd_data.to_csv(outfile, sep='\t', header=True, index=True)
    else:
        for value in pd_data.columns:
            lb = '-'.join(re.split('-', value)[:3])
            list_tmp.append(lb)
        pd_data.to_csv(outfile, sep='\t', header=list_tmp, index=True)

def main():
    parser = argparse.ArgumentParser(description="Trim the TCGA ID to short one(match clinical data)")
    parser.add_argument('-i', help='input File', required=True)
    parser.add_argument('-row', help='trim the row names or col names <<False>>', action='store_true')
    parser.add_argument('-o', help='output matrix <<TrimedMatrix.txt>>', default='TrimedMatrix.txt')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['i'])
    Trim(pd_data, argv['o'], argv['row'])


if __name__ == '__main__':
    main()
