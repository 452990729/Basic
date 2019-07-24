#!/usr/bin/env python2


import sys
import re
import argparse
import pandas as pd


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def GetScore(pd_exp, pd_coef, out):
    pd_exp = pd_exp.loc[pd_coef.index, :].T
    pd_out = pd.DataFrame(index=pd_exp.index, columns=['RiskScore',])
    for i in range(pd_exp.shape[0]):
        score = 0
        for m in range(pd_exp.shape[1]):
            score += pd_exp.iloc[i, m]*pd_coef.iloc[m, 0]
        pd_out.iloc[i, 0] = score
    pd_out.to_csv(out, sep='\t', index=True, header=True)

def main():
    parser = argparse.ArgumentParser(description="cal risk score")
    parser.add_argument('-exp', help='input exp matrix, col is sample, index is genes', required=True)
    parser.add_argument('-coef', help='input coef matrix, col 0 is coef, index is genes', required=True)
    parser.add_argument('-o', help='output <<RiskScore.txt>>', default='RiskScore.txt')
    argv=vars(parser.parse_args())
    pd_exp = ReadData(argv['exp'])
    pd_coef = ReadData(argv['coef'])
    GetScore(pd_exp, pd_coef, argv['o'])


if __name__ == '__main__':
    main()
