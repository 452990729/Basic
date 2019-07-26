#!/usr/bin/env python2


import sys
import re
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ReadAnnot(file_in):
    dict_tmp = {}
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_split = re.split('\t', line.strip())
            for gene in re.split(';', list_split[-1]):
                dict_tmp[gene] = list_split[0]
    return dict_tmp

def MakeData(dict_in, pd_data):
    pd_out = pd.DataFrame(columns=pd_data.columns)
    list_index = []
    for gene in dict_in:
        list_index.append(gene)
        pd_out = pd_out.append(pd_data.loc[dict_in[gene],:])
    pd_out.index=list_index
    pd_out.to_csv('MethSwitchAnno.txt', sep='\t', header=True, index=True)

def main():
    pd_data = ReadData(sys.argv[1])
    dict_tmp = ReadAnnot(sys.argv[2])
    MakeData(dict_tmp, pd_data)


if __name__ == '__main__':
    main()
