#!/mnt/dfc_data1/home/lixuefei/ENV/python3


import sys
import re
import os
import argparse
import modin.pandas as pd


def ReadData(file_in, noheader):
    if not noheader:
        pd_data = pd.read_csv(file_in, sep='\s+', header=0, index_col=0)
    else:
        lb = '.'.join(re.split('\.', os.path.basename(file_in))[:-1])
        print(lb)
        pd_data = pd.read_csv(file_in, sep='\s+', header=None, index_col=0, names=[lb,])
        print(pd_data.head())
    return pd_data

def MergeData(pd1, pd2, method):
    pd_out = pd1.merge(pd2, left_index=True, right_index=True, how=method)
    pd_out = pd_out.fillna(0)
    return pd_out

def MakeFinal(file_list, method, noheader):
    pd_raw = ReadData(file_list[0], noheader)
    for fl in file_list[1:]:
        pd_data = ReadData(fl, noheader)
        pd_raw = MergeData(pd_raw, pd_data, method)
    return pd_raw

def main():
    parser = argparse.ArgumentParser(description="Merge data by columns")
    parser.add_argument('-i', help='input matrix file, seperate by , or file per line', required=True)
    parser.add_argument('-m', help='the merge method <<inner>>', choices=['left', 'right', 'outer', 'inner'], default='inner')
    parser.add_argument('-noheader', help='whether has header', action='store_true')
    parser.add_argument('-o', help='output file<<MergedMatrix.txt>>', default='MergedMatrix.txt')
    argv=vars(parser.parse_args())
    list_fl = []
    if ',' in argv['i']:
        list_fl = re.split(',', argv['i'])
    else:
        with open(argv['i'], 'r') as f:
            for line in f:
                list_fl.append(line.strip())
    pd_out = MakeFinal(list_fl, argv['m'], argv['noheader'])
    pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
