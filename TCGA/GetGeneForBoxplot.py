#!/usr/bin/env python2


import os
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

def HandleFile(file_in, pd_g, pd_c, log, outfile):
    if os.path.exists(file_in):
        with open(file_in, 'r') as f:
            list_g = [re.split('\t', i.strip('\n'))[0] for i in f]
            list_g.remove('')
    else:
        list_g = [file_in]
    pd_c = pd_c.loc[pd_g.columns,:]
    pd_g = pd_g.append(pd_c.T)
    pd_out = pd.DataFrame(columns=['Key', 'Value', 'Class'])
    for key in list_g:
        pd_sub = pd.DataFrame(columns=['Key', 'Value', 'Class'])
        pd_sub['Key'] = pd.DataFrame(key, index=range(pd_g.shape[1]), columns=['Key',]).iloc[:,0]
        if log:
            pd_sub['Value'] = np.array([np.log(m+0.001) for m in pd_g.loc[key,:]])
        else:
            pd_sub['Value'] = np.array(pd_g.loc[key,:])
        pd_sub['Class'] =  np.array(pd_g.loc['Class',:])
        pd_out = pd_out.append(pd_sub)
    pd_out.to_csv(outfile, sep='\t', index=True, header=True)

def main():
    parser = argparse.ArgumentParser(description="Make Matrix For Boxplot")
    parser.add_argument('-e', help='exp file, index are genes, cols are samples', required=True)
    parser.add_argument('-c', help='class file, no header', required=True)
    parser.add_argument('-i', help='input gene list or gene , one gene per line or a gene', required=True)
    parser.add_argument('-log', help='log the value', action='store_true')
    parser.add_argument('-o', help='output file', default='MatrixForBoxplot.txt')
    argv=vars(parser.parse_args())
    pd_g = ReadData(argv['e'])
    pd_c = ReadClass(argv['c'])
    HandleFile(argv['i'], pd_g, pd_c, argv['log'], argv['o'])


if __name__ == '__main__':
    main()
