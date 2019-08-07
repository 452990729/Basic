#!/usr/bin/env python2


import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import mutual_info_score


def GetCorrelation(pd1, pd2, test):
    assert pd1.shape == pd2.shape
    lenth = pd1.shape[0]
    pd_r = pd.DataFrame(index=pd1.index, columns=['Values'])
    if test == 'pearson':
        method = stats.pearsonr
    elif test == 'spearman':
        method = stats.spearmanr
    for i in range(length):
        r, p = method(pd1.iloc[i, :], pd2.iloc[i, :])
        pd_r.iloc[i] = r
    return pd_r

def GetContinusTest(pd1, pd2, test):
    assert pd1.shape[0] == pd2.shape[0]
    length = pd1.shape[0]
    pd_r = pd.DataFrame(index=pd1.index ,columns=['Values'])
    if test == 'T':
        method = stats.ttest_ind
    elif test == 'ks_2samp':
        method = stats.ks_2samp
    elif test == 'ranksums':
        method = stats.ranksums
    elif test == 'signed-rank':
        method = stats.wilcoxon
    for i in range(length):
        s, p = method(pd1.iloc[i, :], pd2.iloc[i, :])
        pd_r.iloc[i] = p
    return pd_r

def GetBinaryTest(pd1, pd2, test):
    print pd1.shape
    print pd2.shape
    assert pd1.shape[1] == pd2.shape[0]
    length = pd1.shape[0]
    pd_r = pd.DataFrame(index=pd1.index ,columns=['Values'])
    if test == 'fisher':
        for i in range(length):
            a,b,c,d = 0,0,0,0
            list_1 = list(np.array(pd1.iloc[i, :].T))
            list_2 = list(np.array(pd2.T)[0])
            for m in range(len(list_1)):
                if list_1[m] == 0 and list_2[m] == 0:
                    a += 1
                elif list_1[m] == 0 and list_2[m] == 1:
                    b += 1
                elif list_1[m] == 1 and list_2[m] == 0:
                    c += 1
                elif list_1[m] == 1 and list_2[m] == 1:
                    d += 1
            table = np.array([[a,b],[c,d]])
            s, p = stats.fisher_exact(table)
            pd_r.iloc[i] = p
    elif test == 'chi2':
        for i in range(length):
            a,b,c,d = 0,0,0,0
            list_1 = list(np.array(pd1.iloc[i, :].T))
            list_2 = list(np.array(pd2.T)[0])
            s, p = stats.chisquare([list_1.count(0), list_1.count(1)],\
                                    [list_2.count(0), list_2.count(1)])
            pd_r.iloc[i] = p
    elif test == 'MI':
        for i in range(length):
            y = np.array(pd2.loc[pd1.columns,:].T)[0]
            print y
            mi = mutual_info_score(pd1.iloc[i, :], y)
            pd_r.iloc[i] = mi
    return pd_r
