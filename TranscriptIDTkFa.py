#!/usr/bin/env python2


import os
import re
import argparse
import pandas as pd
from HTSeq import GFF_Reader,FastaReader

BasePath = os.path.split(os.path.realpath(__file__))[0]
Hg19 = BasePath+'/../../Database/Mode/hsa/hg19/hg19.transcript.gtf'


def ReadGff(GFF):
    dict_gene = {}
    dict_ens = {}
    for line in GFF_Reader(GFF):
        dict_ens[line.attr['transcript_id']] = line
        dict_gene[line.attr['transcript_name']] = line
    return dict_gene, dict_ens

def ReadFa(file_in):
    dict_tmp = {}
    for s in FastaReader(file_in):
        dict_tmp[str(s.name)] = str(s.seq)
    return dict_tmp

def ReadData(file_in, header):
    if header:
        pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    else:
        pd_data = pd.read_csv(file_in, sep='\t', header=None, index_col=0)
    return pd_data

def GetType(dict_gene, dict_ens, pd_data, list_tp):
    if pd_data.index[0].startswith('ENS'):
        dict_in = dict_ens
    else:
        dict_in = dict_gene
    list_tmp = []
    for key in pd_data.index:
        if key in dict_in:
            if dict_in[key].attr['gene_biotype'] in list_tp:
                list_tmp.append(key)
        else:
            print '{} not in annotation file'.format(key)
    pd_out = pd_data.loc[list_tmp,:]
    return pd_out

def Anno(dict_gene, dict_ens, pd_data):
    pd_type = pd.DataFrame(index=pd_data.index ,columns=['GeneBiotype'])
    pd_anno = pd.DataFrame(index=pd_data.index ,columns=['Interpro'])
    if pd_data.index[0].startswith('ENS'):
        pd_id = pd.DataFrame(index=pd_data.index ,columns=['GeneSymbol'])
        dict_in = dict_ens
        lb = 'transcript_name'
    else:
        pd_id = pd.DataFrame(index=pd_data.index ,columns=['Ensemble'])
        dict_in = dict_gene
        lb = 'transcript_id'
    for key in pd_data.index:
        if key in dict_in:
            pd_type.loc[key] = dict_in[key].attr['gene_biotype']
            pd_anno.loc[key] = dict_in[key].attr['interpro']
            pd_id.loc[key] = dict_in[key].attr[lb]
        else:
            pd_type.loc[key] = ''
            pd_anno.loc[key] = ''
            pd_id.loc[key] = ''
    pd_data.insert(0, lb, pd_id)
    pd_data.insert(1, 'GeneBiotype', pd_type)
    pd_data.insert(2, 'Interpro', pd_anno)
    return pd_data

def Switch(dict_gene, dict_ens, dict_data):
    if dict_data.keys()[0].startswith('ENS'):
        dict_in = dict_ens
        lb = 'transcript_name'
    else:
        dict_in = dict_gene
        lb = 'transcript_id'
    list_tmp = []
    for key in dict_data.keys():
        if key in dict_in:
            print '>'+dict_in[key].attr[lb]+'\n'+dict_data[key]
#            list_tmp.append(dict_in[key].attr[lb])
        else:
            print '>NotFind'+'\n'+dict_data[key]
#            list_tmp.append('NotFind')
#    pd_data.index = list_tmp
#    return pd_data[pd_data.index != 'NotFind']

def main():
    parser = argparse.ArgumentParser(description="Annotation Genes/Extract subtype")
    parser.add_argument('method', help='the method used extract/anno/switch', choices=['extract', 'anno', 'switch'], nargs=1)
    parser.add_argument('-m', help='input gene matrix, colomns one is Gene ids', required=True)
    parser.add_argument('-l', help='whether input gene matrix has header <<True>>', action='store_false')
    parser.add_argument('-t', help='extract data type', choices=['LncRNA', 'mRNA', 'sRNA', 'pseudogene', 'miRNA', 'rRNA', 'snoRNA'])
    parser.add_argument('-o', help='output file <<OUTPUT.txt>>', default='OUTPUT.txt')
    argv=vars(parser.parse_args())
#    pd_data = ReadData(argv['m'], argv['l'])
    dict_gene, dict_ens = ReadGff(Hg19)
    if argv['method'][0] == 'extract':
        if argv['t'] == 'LncRNA':
            list_tp = ['lincRNA', '3prime_overlapping_ncrna', 'antisense', 'processed_transcript', 'sense_intronic', 'sense_overlapping']
        elif argv['t'] == 'mRNA':
            list_tp = ['IG_C_gene', 'IG_D_gene', 'IG_J_gene', 'IG_V_gene', 'protein_coding', 'TR_C_gene', 'TR_D_gene', 'TR_J_gene', 'TR_V_gene']
        elif argv['t'] == 'sRNA':
            list_tp = ['miRNA', 'misc_RNA', 'Mt_rRNA', 'Mt_tRNA', 'rRNA', 'snoRNA', 'snRNA']
        elif argv['t'] == 'pseudogene':
            list_tp = ['IG_C_pseudogene', 'IG_J_pseudogene', 'IG_V_pseudogene', 'polymorphic_pseudogene', 'pseudogene', 'TR_J_pseudogene', 'TR_V_pseudogene']
        else:
            list_tp = [argv['t'],]
        pd_out = GetType(dict_gene, dict_ens, pd_data, list_tp)
        pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)
    elif argv['method'][0] == 'anno':
        pd_out = Anno(dict_gene, dict_ens, pd_data)
        pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)
    elif argv['method'][0] == 'switch':
        dict_fa = ReadFa(argv['m'])
        Switch(dict_gene, dict_ens, dict_fa)
#        pd_out = Switch(dict_gene, dict_ens, pd_data)
#        pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()











