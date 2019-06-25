#!/usr/bin/env python2


import os
import sys
import numpy as np
import pandas as pd

BasePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(BasePath+'/Module')
import HpTest

def GetData(file_in):
    pd_data =pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ClassifyContinusTest(X, Y):
    assert X.shape[0] == Y.shape[0]
    X_T = X.T
    Y_uniq = list(set(list(np.array(Y.T)[0])))
    Y_pd1 = Y[Y['Value']==Y_uniq[0]]
    Y_pd2 = Y[Y['Value']==Y_uniq[1]]
    X_T_pd1 = X_T.loc[:, [i for i in Y_pd1.index]]
    X_T_pd2 = X_T.loc[:, Y_pd2.index]
    ks_p = HpTest.GetContinusTest(X_T_pd1, X_T_pd2, 'ks_2samp')
    ranksums_p = HpTest.GetContinusTest(X_T_pd1, X_T_pd2, 'ranksums')
    X_T.insert(0, 'ks_p', ks_p)
    X_T.insert(1, 'ranksums_p', ranksums_p)
    df_filter = X_T[(X_T['ks_p']<=0.5) | (X_T['ranksums_p']<=0.5)].iloc[:, 2:].T
    X_T.to_csv('MulitTestOfFeature.txt', sep='\t', header=True, index=True)
    df_filter.to_csv('FeatureFilterByTest.txt', sep='\t', header=True, index=True)

def ClassifyBinaryTest(X, Y):
    print X.shape
    print Y.shape
    assert X.shape[0] == Y.shape[0]
    X_T = X.T
#    chi2_p = HpTest.GetBinaryTest(X.T, Y, 'chi2')
    fisher_p = HpTest.GetBinaryTest(X_T, Y, 'fisher')
    X_T.insert(0, 'fisher_p', fisher_p)
#    X_T.insert(1, 'chi2_p', chi2_p)
#    df_filter = X_T[(X_T['fisher_p']<=0.5) | (X_T['chi2_p']<=0.5)].iloc[:, 2:].T
    df_filter = X_T[(X_T['fisher_p']<=0.5)].iloc[:, 1:].T
    X_T.to_csv('MulitTestOfFeature.txt', sep='\t', header=True, index=True)
    df_filter.to_csv('FeatureFilterByTest.txt', sep='\t', header=True, index=True)

def main():
    X = GetData(sys.argv[1])
    Y = GetData(sys.argv[2])
    if len(set(list(np.array(X.iloc[:,0].T)))) == 2:
        ClassifyBinaryTest(X, Y)
    else:
        ClassifyContinusTest(X, Y)


if __name__ == '__main__':
    main()
