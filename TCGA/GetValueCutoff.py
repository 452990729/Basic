#!/usr/bin/env python2


import sys
import re
import argparse
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def FilterData(pd_data, cutoff, row):
    rows = pd_data.index
    cols = pd_data.columns
    list_tmp = []
    if row:
        for i in rows:
            for value in pd_data.loc[i, :]:
                if abs(value) >= cutoff:
                    list_tmp.append(i)
                    break
        pd_out = pd_data.loc[list_tmp,:]
    else:
        for i in cols:
            for value in pd_data.loc[:, i]:
                if abs(value) >= cutoff:
                    list_tmp.append(i)
                    break
        pd_out = pd_data.loc[:, list_tmp]
    pd_out.to_csv('FilterData.txt', sep='\t', header=True, index=True)

def main():
    parser = argparse.ArgumentParser(description="Filter data by whole row/col value")
    parser.add_argument('-m', help='input matrix', required=True)
    parser.add_argument('-row', help='filter databy row data or not <<False>>', default=False)
    parser.add_argument('-cutoff', help='cutoff value <<False>>', default=0.95)
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    FilterData(pd_data, argv['cutoff'], argv['row'])


if __name__ == '__main__':
    main()
