#!/usr/bin/env python2


import os
import sys
import re
import argparse
import numpy as np
import pandas as pd
from scipy import stats

BasePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(BasePath+'/../ML/Module')
from HpTest import estimate

def ReadGMT(file_in):
    dict_tmp = {}
    with open(file_in, 'r') as f:
        for line in f:
            list_split = re.split('\t', line.strip())
            dict_tmp[list_split[0]] = list_split[2:]
    return dict_tmp

def MakeFisher(list1, list2, total):
    merge = len(set(list1)&set(list2))
    a = merge
    b = len(list2) - a
    c = len(list1) - a
    d = total - b
    table = np.array([[a,b],[c,d]])
    s, p = stats.fisher_exact(table)
    return s, p

def HandData(file_in, dict_ref):
    with open(file_in, 'r') as f:
        list_gene = [i.strip() for i in f]
    total = len(set(reduce(lambda x,y:x+y, dict_ref.values())))
    pd_out = pd.DataFrame(columns=['count', 'genes', 'pvalue'])
    for key in dict_ref:
        s, p = MakeFisher(list_gene, dict_ref[key], total)
        pd_out.loc[key, 'genes'] = ' '.join(dict_ref[key])
        pd_out.loc[key, 'count'] = len(dict_ref[key])
        pd_out.loc[key, 'pvalue'] = p
    p = np.array(pd_out['pvalue'])
    pd_out['qvalue'] = estimate(p)
    return pd_out

def main():
    parser = argparse.ArgumentParser(description="enrich analysis")
    parser.add_argument('-i', help='input gene file, per gene per line, no header and index', required=True)
    parser.add_argument('-g', help='input gmt file, same as gsea', required=True)
    parser.add_argument('-p', help='filter cutoff(p/qvalue)', type=float, default=0.05)
    parser.add_argument('-f', help='use qvalue to filter', action='store_true')
    parser.add_argument('-o', help='output file <<EnrichFile>>', default='EnrichFile')
    argv=vars(parser.parse_args())
    dict_ref = ReadGMT(argv['g'])
    pd_out = HandData(argv['i'], dict_ref)
    pd_out.to_csv(argv['o']+'.txt', sep='\t', header=True, index=True)
    if argv['f']:
        pd_out[pd_out['qvalue']<argv['p']].to_csv(argv['o']+'.filter.txt', sep='\t', header=True, index=True)
    else:
        pd_out[pd_out['pvalue']<argv['p']].to_csv(argv['o']+'.filter.txt', sep='\t', header=True, index=True)

if __name__ == '__main__':
    main()
