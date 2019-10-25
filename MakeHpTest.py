#!/usr/bin/env python2


import os
import sys
import re
import argparse
import numpy as np
import pandas as pd

BasePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(BasePath+'/ML/Module')
import HpTest

def ReadData(file_in):
    pd_data =pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ReadCls(file_in):
    dict_tmp = {}
    with open(file_in, 'r') as f:
        for line in f:
            list_split = re.split('\t', line.strip())
            if list_split[1] not in dict_tmp:
                dict_tmp[list_split[1]] = [list_split[0],]
            else:
                dict_tmp[list_split[1]] += [list_split[0],]
    return dict_tmp

def MakeTest(pd_data, dict_cls, tp):
    cls = sorted(dict_cls.keys())
    pd_out = pd.DataFrame(index=pd_data.index)
    pd_cls1 = pd_data.loc[:, sorted(dict_cls[cls[0]])]
    pd_cls2 = pd_data.loc[:, sorted(dict_cls[cls[1]])]
    pd_r = HpTest.GetContinusTest(pd_cls1, pd_cls2, tp)
    pd_out[cls[0]+'_mean'] = pd.DataFrame(pd_cls1.mean(1)+0.001)
    pd_out[cls[1]+'_mean'] = pd.DataFrame(pd_cls2.mean(1)+0.001)
    pd_out['log(FoldChange)'] = np.log(pd_out[cls[1]+'_mean']/pd_out[cls[0]+'_mean'])
    pd_out['Pvalue'] = pd_r
    pd_out['Qvalue'] = HpTest.estimate(np.array(pd_r.iloc[:,0].T))
    return pd_out

def Filter(pd_data, pvalue, fold):
    pd_out = pd_data.loc[pd_data.loc[:, 'Qvalue']<pvalue,:]
    pd_out = pd_out.loc[abs(pd_out.loc[:, 'log(FoldChange)'])>fold,:]
    return pd_out

def main():
    parser = argparse.ArgumentParser(description="Hp test")
    parser.add_argument('-m', help='input feature matrix, col are samples, index are features', required=True)
    parser.add_argument('-c', help='input class file, no header and index, col1 are samples, col2 are class', required=True)
    parser.add_argument('-t', help='test method<<ranksums>>', choices=['T', 'ks_2samp', 'ranksums', 'signed-rank'],  default='ranksums')
    parser.add_argument('-p', help='pvalue cutoff <<0.05>>', type=float, default=0.05)
    parser.add_argument('-f', help='foldchange cutoff <<2>>', type=float, default=2)
    parser.add_argument('-o', help='output file <<HpTestFile.txt>>', default='HpTestFile.txt')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    dict_cls = ReadCls(argv['c'])
    pd_out = MakeTest(pd_data, dict_cls, argv['t'])
    pd_out = Filter(pd_out, argv['p'], argv['f'])
    pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
