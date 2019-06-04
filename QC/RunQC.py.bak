#!/usr/bin/env python2


import sys
import re
import os


BasePath = os.path.split(os.path.realpath(__file__))[0]
Adapter1 = open(BasePath+'/Adapter/adapter1.fa', 'r').read().strip()
Adapter2 = open(BasePath+'/Adapter/adapter2.fa', 'r').read().strip()
FASTP = BasePath+'/../../Software/anaconda2/envs/fastp-0.20.0/bin/fastp'


class Read(object):
    def __init__(self, name):
        self.name = name
        self.read1 = 0
        self.read2 = 0
        self.out1 = self.name+'_1.clean.fq.gz'
        self.out2 = self.name+'_2.clean.fq.gz'
        self.adapter1 = Adapter1
        self.adapter2 = Adapter2

    def UpdateRead(self, tp, path):
        if tp == 'read1':
            self.read1 = path
        elif tp == 'read2':
            self.read2 = path

    def UpdateAdapter(self, tp, path):
        if tp == 'adapter1':
            self.adapter1 = path
        elif tp == 'adapter2':
            self.adapter2 = path

    def CMD(self, outpath):
        cmd = ' '.join([FASTP, '-i', self.read1, '--adapter_sequence', self.adapter1,\
                       '-o', outpath+'/'+self.out1, '-I', self.read2, '--adapter_sequence_r2',\
                       self.adapter2, '-O', outpath+'/'+self.out2, '-j',\
                        outpath+'/'+self.name+'_QC_report.json', '-h',\
                       outpath+'/'+self.name+'_QC_report.html'])
        return cmd


def GetSample(path_in):
    dict_sample = {}
    root, dirs, files = next(os.walk(path_in))
    for fl in files:
        list_tmp = re.findall('(.*)_([1,2])\..*\.(.*)', fl)[0]
        if list_tmp[0] not in dict_sample:
            dict_sample[list_tmp[0]] = Read(list_tmp[0])
        ob = dict_sample[list_tmp[0]]
        fl_path = os.path.join(root, fl)
        if list_tmp[2] == 'gz':
            if list_tmp[1] == '1':
                ob.UpdateRead('read1', fl_path)
            elif list_tmp[1] == '2':
                ob.UpdateRead('read2', fl_path)
        elif list_tmp[2] == 'adapter':
            if list_tmp[1] == '1':
                ob.UpdateAdapter('adapter1', fl_path)
            elif list_tmp[1] == '2':
                ob.UpdateAdapter('adapter2', fl_path)
    return dict_sample.values(), os.path.split(root)[1]

def QC(list_in, outpath, library):
    libpath = os.path.join(outpath, library)
    if os.path.exists(libpath):
        os.rmdir(libpath)
    os.mkdir(libpath)
    for ob in list_in:
        os.system(ob.CMD(libpath))
    os.system('zcat {}/*_1.clean.fq.gz > {}'.format(libpath, os.path.join(outpath, library+'_1.clean.fq')))
    os.system('zcat {}/*_2.clean.fq.gz > {}'.format(libpath, os.path.join(outpath, library+'_2.clean.fq')))
    os.system('gzip {}'.format(os.path.join(outpath, library+'_1.clean.fq')))
    os.system('gzip {}'.format(os.path.join(outpath, library+'_2.clean.fq')))

def main():
    list_sample, library = GetSample(sys.argv[1])
    QC(list_sample, sys.argv[2], library)


if __name__ == '__main__':
    main()

