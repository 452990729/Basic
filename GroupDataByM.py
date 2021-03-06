#!/usr/bin/env python2


import os
import sys
import re
import argparse
import pandas as pd


def ReadMatrix(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ReadClass(file_in):
    dict_tmp = {}
    if os.path.exists(file_in):
        with open(file_in, 'r') as f:
            for line in f:
                list_split = re.split('\t', line.strip('\n'))
                if list_split[0]:
                    if list_split[1] not in dict_tmp:
                        dict_tmp[list_split[1]] = [list_split[0],]
                    else:
                        dict_tmp[list_split[1]] += [list_split[0],]
    return dict_tmp

def HandleData(dict_class, pd_matrix, tp, outfile, label):
    keys = sorted(dict_class.keys())
    if label:
        index = re.split(':', label)
    else:
        index = pd_matrix.index
    pd_out = pd.DataFrame()
    if len(keys) == 0:
        dict_class['value'] = list(pd_matrix.columns)
        keys = dict_class.keys()
    for key in keys:
        pd_sub = pd_matrix.loc[:, dict_class[key]]
        if tp == 'mean':
            pd_1 = pd.DataFrame(pd_sub.mean(1))
        elif tp == 'median':
            pd_1 = pd.DataFrame(pd_sub.median(1))
        pd_1.columns=[key, ]
        pd_out = pd_out.append(pd_1.T)
#    pd_out.index = index
    pd_out.T.to_csv(outfile, sep='\t', index=True, header=True)

def main():
    parser = argparse.ArgumentParser(description="cal mean/median of feature by sample class")
    parser.add_argument('-c', help='the sample class file<<none>>', default='none')
    parser.add_argument('-i', help='the input matrix', required=True)
    parser.add_argument('-m', help='mean or median <<mean>>', choices=['mean', 'median'], default='mean')
    parser.add_argument('-o', help='output file<<TransformedMatrix.txt>>', default='TransformedMatrix.txt')
    parser.add_argument('-l', help='output file columns, sep by : <<False>>', default=False)
    argv=vars(parser.parse_args())
    pd_matrix = ReadMatrix(argv['i'])
    dict_class = ReadClass(argv['c'])
    HandleData(dict_class, pd_matrix, argv['m'], argv['o'], argv['l'])


if __name__ == '__main__':
    main()
