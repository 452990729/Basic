#!/usr/bin/env python2

import re
import os
import argparse
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def GetClass(pd_data):
    list_c = []
    list_n = []
    for sample in pd_data.columns:
        tp = int(re.findall('\w+\-\w+\-\w+\-(\d+)\w\-', sample)[0])
        if tp>=1 and tp<=9:
            list_c.append(sample)
        elif tp>=10 and tp<=29:
            list_n.append(sample)
        else:
            print '{} cannot classify'
    return list_c, list_n

def SelectDup(list_in):
    list_out = []
    list_lb = []
    for sample in list_in:
        lb = '-'.join(re.split('-', sample)[:4])[:-1]
        if lb not in list_lb:
            list_lb.append(lb)
            list_out.append(sample)
    return list_lb, list_out

def Classify(pd_data, list_c, list_n, outpath):
    out = open(os.path.join(outpath, 'SampleClass.txt'), 'w')
    list_c_lb, list_c_out = SelectDup(list_c)
    list_n_lb, list_n_out = SelectDup(list_n)
    for value in list_c_lb:
        out.write('{}\tCancer\n'.format(value))
    for value in list_n_lb:
        out.write('{}\tNormal\n'.format(value))
    out.close()
    pd_c = pd_data.loc[:, list_c_out]
    pd_n = pd_data.loc[:, list_n_out]
    pd_a = pd_data.loc[:, list_c_out+list_n_out]
    pd_c.columns = list_c_lb
    pd_n.columns = list_n_lb
    pd_a.columns = list_c_lb+list_n_lb
    pd_c.to_csv(os.path.join(outpath, 'CancerMitrix.txt'), sep='\t', header=True, index=True)
    pd_n.to_csv(os.path.join(outpath, 'NormalMitrix.txt'), sep='\t', header=True, index=True)
    pd_a.to_csv(os.path.join(outpath, 'AllMitrix.txt'), sep='\t', header=True, index=True)

def main():
    parser = argparse.ArgumentParser(description="Clssify sample type from TCGA id")
    parser.add_argument('-m', help='input TCGA Matrix, header in row1', required=True)
    parser.add_argument('-o', help='output path <<.>>', default='.')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    list_c, list_n = GetClass(pd_data)
    Classify(pd_data, list_c, list_n, argv['o'])


if __name__ == '__main__':
    main()



