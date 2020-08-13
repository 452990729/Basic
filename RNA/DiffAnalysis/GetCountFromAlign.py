#!/usr/bin/env python2


import sys
import re
import os
import argparse
import pandas as pd
from LocalJobsEX import LaunchJobs

BasePath = os.path.split(os.path.realpath(__file__))[0]
HtseqCount = BasePath+'/htseq-count'

def MakeCountShell(list_align, gff, outpath, featuretype,\
                   idattr, mode, order, stranded):
    list_shell = []
    list_count = []
    for fl in list_align:
        if fl.endswith('sam'):
            tp = 'sam'
        elif fl.endswith('bam'):
            tp = 'bam'
        else:
            print 'file type is not sam/bam '
            break
        lb = re.split('\.', os.path.basename(fl))[0]
        out = open(os.path.join(outpath, lb+'.sh'), 'w')
        out_count = os.path.join(outpath, lb+'.count')
        shell = '{} -f {} -r {} -s {} -t {} -i {} -m {} -q {} {} > {}'\
                .format(HtseqCount, tp, order, stranded, featuretype,\
                       idattr, mode, fl, gff, out_count)
        out.write(shell)
        out.close()
        list_shell.append(os.path.join(outpath, lb+'.sh'))
        list_count.append(out_count)
    return list_shell, list_count

def RunShell(list_shell, list_count, outpath, core):
    LaunchJobs(list_shell, num=core)
    m = 0
    for count_fl in list_count:
        lb = re.split('\.', os.path.basename(count_fl))[0]
        if m == 0:
            pd_out = pd.read_csv(count_fl, sep='\t', header=None, index_col=0, names=[lb,])
        else:
            pd_out[lb] = pd.read_csv(count_fl, sep='\t', header=None, index_col=0)
        m = 1
    pd_out.iloc[:-5, :].to_csv(os.path.join(outpath, 'FinalReadsCount.txt'), sep='\t', header=True, index=True)
    os.system('rm {}/*.sh*'.format(outpath))
    os.system('rm {}/*.count'.format(outpath))

def main():
    parser = argparse.ArgumentParser(description="Get ReadCounts From Bam/Sam by gff")
    parser.add_argument('-i', help='the input bam files, seperate by ,', required=True)
    parser.add_argument('-g', help='the input gff file', required=True)
    parser.add_argument('-o', help='the output path', required=True)
    parser.add_argument('-t', help='the threads used <<6>>', default=6)
    parser.add_argument('-featuretype', help='feature type (3rd column in GFF file) to be used <<exon>>'\
                        , default='exon')
    parser.add_argument('-idattr', help='GFF attribute to be used as feature ID <<gene_id>>', default='gene_id')
    parser.add_argument('-mode', help='mode to handle reads overlapping more than one feature,\
                        union/intersection-strict/intersection-nonempty <<union>>',\
                        choices=['union', 'intersection-strict', 'intersection-nonempty'], default='union')
    parser.add_argument('-order', help='\'pos\' or \'name\'. Sorting order of <alignment_file> <<name>>',\
                        choices=['pos', 'name'], default='name')
    parser.add_argument('-stranded', help='whether the data is from a strand-specific assay <<no>>',\
                        choices=['yes', 'no'], default='no')
    argv=vars(parser.parse_args())
    list_shell, list_count = MakeCountShell(re.split(',', argv['i']), argv['g'], argv['o'],\
                                           argv['featuretype'], argv['idattr'], argv['mode'],\
                                           argv['order'], argv['stranded'])
    RunShell(list_shell, list_count, argv['o'], argv['t'])


if __name__ == '__main__':
    main()
