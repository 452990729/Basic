#!/usr/bin/env python2


import sys
import re
import argparse
from HTSeq import FastaReader

def ReadFasta(file_in):
    dict_out = {}
    for s in FastaReader(file_in):
        dict_out[s.name] = str(s.seq)
    return dict_out

def ReadGeneFamily(file_in, dict_fa, outfile):
    out = open(outfile, 'w')
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_split = re.split('\t', line.strip())
            out.write('>{}\n{}\n'.format(list_split[0], dict_fa[re.split(',', list_split[2])[0]]))
    out.close()

def main():
    parser = argparse.ArgumentParser(description="Get gene family fasta from gene family result")
    parser.add_argument('-f', help='input fasta file', required=True)
    parser.add_argument('-g', help='GeneFamily file', required=True)
    parser.add_argument('-o', help='output file<<Out.fasta>>', default='Out.fasta')
    argv=vars(parser.parse_args())
    dict_fa = ReadFasta(argv['f'])
    ReadGeneFamily(argv['g'], dict_fa, argv['o'])


if __name__ == '__main__':
    main()

