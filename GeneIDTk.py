#!/usr/bin/env python2


import re
import argparse
import pandas as pd
from HTSeq import GFF_Reader

Hg19 = '/home/lixuefei/Database/Mode/hsa/hg19/hg19.gene.gtf'


def ReadGff():
    dict_gene = {}
    dict_ens = {}
    for line in GFF_Reader(Hg19):
        dict_gene[line.attr['gene_id']] = line
        dict_gene[line.attr['gene_name']] = line
    return dict_gene, dict_ens

def ReadData(file_in, header):
    if header:
        pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    else:
        pd_data = pd.read_csv(file_in, sep='\t', header=None, index_col=0)
    return pd_data

def GetType(dict_in, pd_data, list_tp):
    list_tmp = []
    for key in pd_data.index:
        if dict_in[key].attr['gene_biotype'] in list_tp::
            list_tmp.append(key)
    pd_out = pd_data.loc[list_tmp,:]
    return pd_out

def Anno(dict_gene, dict_ens, pd_data):

    pd_id = pd.DataFrame(index=pd_data.index ,columns=['Values'])
    for key in pd_data.index:
        if key in dict_in:



