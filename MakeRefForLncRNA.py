#!/usr/bin/env python2


import os
import re
import sys
from HTSeq import GFF_Reader


def ReadGff(GFF):
    list_lnc = ['lincRNA', '3prime_overlapping_ncrna', 'antisense', 'processed_transcript', 'sense_intronic', 'sense_overlapping', 'lncRNA']
    dict_gene = {}
    dict_ens = {}
    lnc = open('lncRNARef.gtf', 'w')
    for line in GFF_Reader(GFF):
        if line.attr['gene_biotype'] in list_lnc:
            line.attr['gene_biotype'] = 'lncRNA'
            lnc.write(line.get_gff_line().strip()+'\n')
        elif line.attr['gene_biotype'] == 'protein_coding':
            line.attr['gene_biotype'] = 'mRNA'
            lnc.write(line.get_gff_line().strip()+'\n')

ReadGff(sys.argv[1])
