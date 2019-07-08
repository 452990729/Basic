#!/usr/bin/env python2


import re
import argparse
import pandas as pd


def ReadTotal(file_in, header=True):
    if header:
        pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    else:
        pd_data = pd.read_csv(file_in, sep='\t', header=None, index_col=0)
    return pd_data

def HandleID(file_in):
    list_out = []
    with open(file_in, 'r') as f:
        for line in f:
            line = line.strip('\m')
            list_split = re.split('\t', line)
            if list_split[0] != '':
                list_out.append(list_split[0])
    return list_out

def ExtractData(pd_data, list_id, colname, col=False):
    if col:
        pd_out = pd_data.loc[:, list_id]
    else:
        if colname:
            pd_out = pd_data.loc[pd_data[colname].isin(list_id)]
        else:
            pd_out = pd_data.loc[list_id, :]
    pd_out.to_csv('ExtractData.txt', sep='\t', header=True, index=True)

def main():
    parser = argparse.ArgumentParser(description="extract data by id (col/row)")
    parser.add_argument('-m', help='input matrix data', required=True)
    parser.add_argument('-i', help='input input id data, more than 1 columns', required=True)
    parser.add_argument('-col', help='extract by clo or by row', action='store_true')
    parser.add_argument('-colname', help='extract row by the col label if false, use index<<False>>', default=False)
    parser.add_argument('-header', help='input matrix data has header or not <<True>>', default=True)
    argv=vars(parser.parse_args())
    pd_data = ReadTotal(argv['m'], argv['header'])
    list_id = HandleID(argv['i'])
    ExtractData(pd_data, list_id, argv['colname'], argv['col'])


if __name__ == '__main__':
    main()
