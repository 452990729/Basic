#!/usr/bin/env python2


import sys
import re
import argparse
import pandas as pd


def ReadMatrix(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ReadClass(file_in):
    dict_tmp = {}
    with open(file_in, 'r') as f:
        for line in f:
            list_split = re.split('\t', line.strip())
            if list_split[1] not in dict_tmp:
                dict_tmp[list_split[1]] = [list_split[0],]
            else:
                dict_tmp[list_split[1]] += [list_split[0],]
    return dict_tmp

def HandleData(dict_class, pd_matrix, tp):
    keys = sorted(dict_class.keys())
    pd_out = pd.DataFrame(columns=pd_matrix.index)
    for key in keys:
        pd_sub = pd_matrix.loc[:, dict_class[key]]
        if tp == 'mean':
            pd_1 = pd.DataFrame(pd_sub.mean(1))
        elif tp == 'median':
            pd_1 = pd.DataFrame(pd_sub.median(1))
        pd_1.columns=[key, ]
        pd_out = pd_out.append(pd_1.T)
    pd_out.T.to_csv('TransformedMatrix.txt', sep='\t', index=True, header=True)

def main():
    parser = argparse.ArgumentParser(description="cal mean/median of feature by sample class")
    parser.add_argument('-c', help='cox result file', required=True)
    parser.add_argument('-i', help='the input matrix', required=True)
    parser.add_argument('-m', help='mean or median', choices=['mean', 'median'], default='mean')
    argv=vars(parser.parse_args())
    pd_matrix = ReadMatrix(argv['i'])
    dict_class = ReadClass(argv['c'])
    HandleData(dict_class, pd_matrix, argv['m'])


if __name__ == '__main__':
    main()
