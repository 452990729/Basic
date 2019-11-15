#!/usr/bin/env python2


import os
import re
import argparse
import pandas as pd
from HTSeq import GFF_Reader,FastaReader

BasePath = os.path.split(os.path.realpath(__file__))[0]


def ReadGff(GFF):
    list_gff = []
    for line in GFF_Reader(GFF):
        list_gff.append(line)
    return list_gff

def GetType(list_gff, list_tp, lb, tp):
    out = open(lb+'_'+tp+'.gtf', 'w')
    for line in list_gff:
        if line.attr['gene_biotype'] in list_tp:
            out.write(line.get_gff_line().strip()+'\n')
    out.close()

def main():
    parser = argparse.ArgumentParser(description="Annotation Genes/Extract subtype")
    parser.add_argument('-g', help='input gff file', required=True)
    parser.add_argument('-t', help='extract data type', choices=['LncRNA', 'mRNA', 'sRNA', 'pseudogene', 'miRNA', 'rRNA', 'snoRNA'])
    parser.add_argument('-l', help='output label <<Sample>>', default='Sample')
    argv=vars(parser.parse_args())
    list_gff = ReadGff(argv['g'])
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
    GetType(list_gff, list_tp, argv['l'], argv['t'])


if __name__ == '__main__':
    main()











