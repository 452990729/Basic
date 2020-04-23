#!/usr/bin/env python2


import os
import sys
import re
import pandas as pd


BasePath = os.path.split(os.path.realpath(__file__))[0]
Gene_len = BasePath +'/../../../Database/Mode/hsa/hg19/hg19.exon.merge.length'

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ReadLen(file_in):
    dict_tmp = {}
    with open(file_in, 'r') as f:
        for line in f:
            list_split = re.split('\t', line.strip())
            dict_tmp[list_split[0]] = round(float(list_split[1])/1000, 4)
    return dict_tmp

def Count2FPKM(count, total, length):
    return round(count/(total*length), 2)

def Process(pd_data, dict_len):
    list_tmp = []
    for i in pd_data.index:
        if i in dict_len:
            list_tmp.append(i)
        else:
            print str(i)+' not in config'
    pd_out = pd.DataFrame(index=list_tmp, columns=pd_data.columns)
    pd_data = pd_data.loc[list_tmp, :]
    total = round(pd_data.to_numpy().sum()/1000000, 4)
    for index in pd_data.index:
        for column in pd_data.columns:
            pd_out.loc[index, column] = Count2FPKM(pd_data.loc[index, column], total, dict_len[index])
    return pd_out

def main():
    pd_data = ReadData(sys.argv[1])
    dict_len = ReadLen(Gene_len)
    pd_out = Process(pd_data, dict_len)
    pd_out.to_csv('Gene.FPKM', sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
