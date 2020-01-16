#!/usr/bin/env python2


import sys
import argparse
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def FilterData(pd_data, tp):
    if tp == 'index':
        pd_out = pd_data[~pd_data.index.duplicated()]
        return pd_out
    else:
        pd_out = pd_data.drop_duplicates(subset=tp)
    return pd_out

def main():
    parser = argparse.ArgumentParser(description="remove duplicate line of pandas DataFrame")
    parser.add_argument('-m', help='input matrix, with header and index', required=True)
    parser.add_argument('-t', help=' which columns to filter <<index>>', default='index')
    parser.add_argument('-o', help='output file <<DataFrameDedup.txt>>', default='DataFrameDedup.txt')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    pd_out = FilterData(pd_data, argv['t'])
    pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
