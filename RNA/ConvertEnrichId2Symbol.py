#!/usr/bin/env python2


import re
import os
import argparse

BasePath = os.path.split(os.path.realpath(__file__))[0]

def MakeRef(file_in):
    dict_tmp = {}
    with open(file_in, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                list_split = re.split('\t', line)
                dict_tmp[list_split[1]] = list_split[2]
    return dict_tmp

def HandleEnrichID(file_in, dict_ref, outfile):
    out = open(outfile, 'w')
    index = 0
    with open(file_in, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if index == 0:
                out.write(line+'\n')
            else:
                list_split = re.split('\t', line)
                sft = '/'.join([dict_ref[i] for i in re.split('\/', list_split[-2])])
                out.write('\t'.join(list_split[:-2]+[sft,]+list_split[-1:])+'\n')
            index += 1
    out.close()

def main():
    parser = argparse.ArgumentParser(description="convert enrich.R result to gene symbol")
    parser.add_argument('-i', help='input data', required=True)
    parser.add_argument('-o', help='output file<<EnrichConvert.txt>>', default='EnrichConvert.txt')
    argv=vars(parser.parse_args())
    dict_ref = MakeRef(BasePath+'/../../../Database/Mode/hsa/hg19/Homo_sapiens.gene_info')
    HandleEnrichID(argv['i'], dict_ref, argv['o'])


if __name__ == '__main__':
    main()
