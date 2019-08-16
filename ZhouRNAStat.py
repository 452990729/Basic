#!/usr/bin/env python2


import sys
import re
from glob import glob

def QCStat(file_in):
    with open(file_in, 'r') as f:
        F,T = re.findall('Done : (\d+) of (\d+)', f.read())[0]
    return F+'\t'+T+'\t'+str(int(T)-int(F))+'\t'+\
            str(round(float(int(T)-int(F))*100/int(T), 2))

def DupStat(file_in):
    with open(file_in, 'r') as f:
        string = f.read()
        U,D,R = re.findall('Unique\s+\:\s+(\d+)\nDuplicate\s+:\s+(\d+)\n\s+\((\w+\.\w+)', string)[0]
    return U+'\t'+D+'\t'+str(round(float(R), 2))

def MapStat(file_in):
    with open(file_in, 'r') as f:
        string = f.read()
        T = re.findall('Number of input reads \|\t(\d+)\n', string)[0]
        U = re.findall('Uniquely mapped reads number \|\t(\d+)\n', string)[0]
        R = re.findall('Uniquely mapped reads % \|\t(.+)\n', string)[0]
    return T+'\t'+U+'\t'+R

def main():
    sample_path = sorted(glob(sys.argv[1]+'/*/'))
    print 'Data filtering'
    print ' \tFiltered_Flagment\tTotal_Flagment\tPassed_Flagment\tPassRate(%)'
    for sample in sample_path:
        QC = glob(sample+'/00datafilter/*.trim.err')[0]
        lb = re.split('\/', sample)[-2]
        print lb+'\t'+QCStat(QC)
    print '\nDuplication rate'
    print ' \tUnique Fragment\tDuplicate\tDuplication Rate(%)'
    for sample in sample_path:
        Dup = glob(sample+'/00datafilter/*.Trim.RD.log')[0]
        lb = re.split('\/', sample)[-2]
        print lb+'\t'+DupStat(Dup)
    print '\nAlignment'
    print ' \tTotal_Flagment\tAligned_Flagment\tAlignmentRate(%)'
    for sample in sample_path:
        Map = glob(sample+'/01alignment/*.Log.final.out')[0]
        lb = re.split('\/', sample)[-2]
        print lb+'\t'+MapStat(Map)


if __name__ == '__main__':
    main()
