#!/usr/bin/env python2


import argparse
import re
import pandas as pd


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def DropData(pd_data, threshold, row):
    if row:
        pd_data = pd_data.T
        pd_out = pd_data.loc[:, pd_data.std() > threshold].T
    else:
        pd_out = pd_data.loc[:, pd_data.std() > threshold]
    return pd_out

def main():
    parser = argparse.ArgumentParser(description="remove low standard deviation of dataframe")
    parser.add_argument('-m', help='input matrix data', required=True)
    parser.add_argument('-row', help='cal standard deviation by row<<row>>', action='store_true')
    parser.add_argument('-t', help='filter threshold standard deviation<<0>>', type=float, default=0)
    parser.add_argument('-o', help='output file<<RemoveStandardDeviation.txt>>', default='RemoveStandardDeviation.txt')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    pd_out = DropData(pd_data, argv['t'], argv['row'])
    pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
