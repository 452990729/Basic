#!/usr/bin/env python2


import sys
import re
import argparse
import numpy as np
import pandas as pd


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ReadClass(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', names=['Class',], index_col=0)
    return pd_data

def HandleFile(file_in, pd_g, pd_c):
    with open(file_in, 'r') as f:
        list_g = [i.strip() for i in f]
    pd_c = pd_c.loc[pd_g.columns,:]
    pd_g = pd_g.append(pd_c.T)
    pd_out = pd.DataFrame(columns=['Key', 'Value', 'Class'])
    for key in list_g:
        pd_sub = pd.DataFrame(columns=['Key', 'Value', 'Class'])
        pd_sub['Key'] = pd.DataFrame(key, index=range(pd_g.shape[1]), columns=['Key',]).iloc[:,0]
        pd_sub['Value'] = np.array(pd_g.loc[key,:])
        pd_sub['Class'] =  np.array(pd_g.loc['Class',:])
        pd_out = pd_out.append(pd_sub)
    pd_out.to_csv('MatrixForBoxplot.txt', sep='\t', index=True, header=True)

def main():
    parser = argparse.ArgumentParser(description="Make Matrix For Boxplot")
    parser.add_argument('-e', help='exp file, index are genes, cols are samples', required=True)
    parser.add_argument('-c', help='class file, no header', required=True)
    parser.add_argument('-i', help='input gene list , one gene per line', required=True)
    argv=vars(parser.parse_args())
    pd_g = ReadData(argv['e'])
    pd_c = ReadClass(argv['c'])
    HandleFile(argv['i'], pd_g, pd_c)


if __name__ == '__main__':
    main()
