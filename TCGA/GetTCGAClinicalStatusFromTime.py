#!/usr/bin/env python2


import argparse
import pandas as pd


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def MakeData(pd_data):
    list_y1 = []
    list_y3 = []
    list_y5 = []
    pd_out = pd.DataFrame(index=pd_data.index)
    for index in pd_data.index:
        if pd_data.loc[index, 'OS'] <365:
            list_y1.append(1)
        else:
            list_y1.append(0)
        if pd_data.loc[index, 'OS'] < 365*3:
            list_y3.append(1)
        else:
            list_y3.append(0)
        if pd_data.loc[index, 'OS'] < 365*5:
            list_y5.append(1)
        else:
            list_y5.append(0)
    pd_out['1 year'] = list_y1
    pd_out['3 years'] = list_y3
    pd_out['5 years'] = list_y5
    return pd_out

def main():
    parser = argparse.ArgumentParser(description="make 1/3/5 years status from TCGA clinical file")
    parser.add_argument('-s', help='input TCGA clinical matrix, col are features, index are samples, include OS/status', required=True)
    parser.add_argument('-o', help='output file<<TCGAStatus.txt>>', default='TCGAStatus.txt')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['s'])
    pd_out = MakeData(pd_data)
    pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
