#!/usr/bin/env python2


import sys
import re
import argparse
import pandas as pd


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def MergeData(pd1, pd2, method):
    pd_out = pd1.merge(pd2, left_index=True, right_index=True, how=method)
    pd_out = pd_out.fillna(0)
    return pd_out

def MakeFinal(file_list, method):
    pd_raw = ReadData(file_list[0])
    for fl in file_list[1:]:
        pd_data = ReadData(fl)
        pd_raw = MergeData(pd_raw, pd_data, method)
    return pd_raw

def main():
    parser = argparse.ArgumentParser(description="Merge data by columns")
    parser.add_argument('-i', help='input matrix file, seperate by ,', required=True)
    parser.add_argument('-m', help='the merge method <<inner>>', choices=['left', 'right', 'outer', 'inner'], default='inner')
    parser.add_argument('-o', help='output file<<MergedMatrix.txt>>', default='MergedMatrix.txt')
    argv=vars(parser.parse_args())
    pd_out = MakeFinal(re.split(',', argv['i']), argv['m'])
    pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
