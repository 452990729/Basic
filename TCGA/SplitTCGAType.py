#!/usr/bin/env python2

import re
import os
import argparse
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def GetClass(pd_data):
    list_c = []
    list_n = []
    for sample in pd_data.columns:
        tp = int(re.findall('\w+\-\w+\-\w+\-(\d+)', sample)[0])
        if tp>=1 and tp<=9:
            list_c.append(sample)
        elif tp>=10 and tp<=29:
            list_n.append(sample)
        else:
            print '{} cannot classify'
    return list_c, list_n

def Classify(pd_rc, pd_rf, pd_m, list_c, list_n, outpath):
    AllSampleClass = open(os.path.join(outpath, 'AllSampleClass.txt'), 'w')
    TestSampleClass = open(os.path.join(outpath, 'TestSampleClass.txt'), 'w')
    TrainSampleClass = open(os.path.join(outpath, 'TrainSampleClass.txt'), 'w')
    TrainCancerClass = open(os.path.join(outpath, 'TrainCancerClass.txt'), 'w')
    m = 0
    list_train = []
    list_test = []
    AllSampleClass.write('\tType\n')
    TestSampleClass.write('\tType\n')
    TrainSampleClass.write('\tType\n')
    TrainCancerClass.write('\tType\n')
    for value in list_c:
        m += 1
        AllSampleClass.write('{}\tCancer\n'.format(value))
        if m <= len(list_c)/2:
            TrainSampleClass.write('{}\tCancer\n'.format(value))
            TrainCancerClass.write('{}\tCancer\n'.format(value))
            list_train.append(value)
        else:
            TestSampleClass.write('{}\tCancer\n'.format(value))
            list_test.append(value)
    for value in list_n:
        AllSampleClass.write('{}\tNormal\n'.format(value))
        TrainSampleClass.write('{}\tNormal\n'.format(value))
        list_train.append(value)
    AllSampleClass.close()
    TestSampleClass.close()
    TrainSampleClass.close()
    TrainCancerClass.close()
    pd_rc = pd_rc[~pd_rc.index.duplicated()]
    pd_rf = pd_rf[~pd_rf.index.duplicated()]
    pd_rc.loc[:, list_train].to_csv(os.path.join(outpath, 'TrainRNACount.txt'), sep='\t', header=True, index=True)
    pd_rf.loc[:, list_train].to_csv(os.path.join(outpath, 'TrainRNAFPKM.txt'), sep='\t', header=True, index=True)
    pd_rf.loc[:, list_test].to_csv(os.path.join(outpath, 'TestRNAFPKM.txt'), sep='\t', header=True, index=True)
    pd_m.loc[:, list_train].to_csv(os.path.join(outpath, 'TrainMeth.txt'), sep='\t', header=True, index=True)
    pd_m.loc[:, list_test].to_csv(os.path.join(outpath, 'TestMeth.txt'), sep='\t', header=True, index=True)

def main():
    parser = argparse.ArgumentParser(description="Split sample to Train and test set")
    parser.add_argument('-rc', help='input RNACOUNT matrix', required=True)
    parser.add_argument('-rf', help='input RNAFPKM matrix', required=True)
    parser.add_argument('-m', help='input METH matrix', required=True)
    parser.add_argument('-o', help='output path <<.>>', default='.')
    argv=vars(parser.parse_args())
    pd_rc = ReadData(argv['rc'])
    pd_rf = ReadData(argv['rf'])
    pd_m = ReadData(argv['m'])
    list_c, list_n = GetClass(pd_rc)
    Classify(pd_rc, pd_rf, pd_m, list_c, list_n, argv['o'])


if __name__ == '__main__':
    main()



