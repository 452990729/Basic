#!/usr/bin/env python2


import sys
import re
import argparse
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def GetTrimData(pd_in):
    list_tmp = []
    list_sample = []
    for sample in pd_in.columns:
        label = re.findall('(\w+\-\w+\-\w+\-\d+)', sample)[0]
        if label not in list_tmp:
            list_tmp.append(label)
            list_sample.append(sample)
    pd_out  = pd_in.loc[:, list_sample]
    pd_out.columns = list_tmp
    pd_out = pd_out.dropna(axis=0, how='all')
    return pd_out

def MergeData(pd_RNAc, pd_RNAf, pd_meth, pd_clinical):
    list_l = list(set(pd_RNAc.columns)&set(pd_meth.columns))
    list_r = []
    for sample in list_l:
        lb = '-'.join(re.split('-', sample)[:3])
        if lb in pd_clinical.index:
            list_r.append(sample)
    pd_RNAc = pd_RNAc.loc[:, list_r]
    pd_RNAf = pd_RNAf.loc[:, list_r]
    pd_meth = pd_meth.loc[:, list_r]
    return pd_RNAc, pd_RNAf, pd_meth

def main():
    parser = argparse.ArgumentParser(description="Overlap RNA METH CLINECAL Data")
    parser.add_argument('-s', help='input usefule clinical matrix', required=True)
    parser.add_argument('-rc', help='input RNACOUNT matrix', required=True)
    parser.add_argument('-rf', help='input RNAFPKM matrix', required=True)
    parser.add_argument('-m', help='input METH matrix', required=True)
    argv=vars(parser.parse_args())
    pd_s = ReadData(argv['s'])
    pd_rc = ReadData(argv['rc'])
    pd_rf = ReadData(argv['rf'])
    pd_m = ReadData(argv['m'])
    pd_rc = GetTrimData(pd_rc)
    pd_rf = GetTrimData(pd_rf)
    pd_m = GetTrimData(pd_m)
    pd_RNAc, pd_RNAf, pd_meth = MergeData(pd_rc, pd_rf, pd_m, pd_s)
    pd_RNAc.to_csv('TCGA-RNACount.txt', sep='\t', header=True, index=True)
    pd_RNAf.to_csv('TCGA-RNAFPKM.txt', sep='\t', header=True, index=True)
    pd_meth.to_csv('TCGA-METH.txt', sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
