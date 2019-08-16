#!/usr/bin/env python2


import numpy as np
import pandas as pd
import scipy as sp
from scipy import stats
from scipy import interpolate
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

def estimate(pv, m=None, verbose=False, lowmem=False, pi0=None):
    """
    Estimates q-values from p-values

    Args
    =====

    m: number of tests. If not specified m = pv.size
    verbose: print verbose messages? (default False)
    lowmem: use memory-efficient in-place algorithm
    pi0: if None, it's estimated as suggested in Storey and Tibshirani, 2003.
         For most GWAS this is not necessary, since pi0 is extremely likely to be
         1

    """
    assert(pv.min() >= 0 and pv.max() <= 1), "p-values should be between 0 and 1"

    original_shape = pv.shape
    pv = pv.ravel()  # flattens the array in place, more efficient than flatten()

    if m is None:
        m = float(len(pv))
    else:
        # the user has supplied an m
        m *= 1.0

    # if the number of hypotheses is small, just set pi0 to 1
    if len(pv) < 100 and pi0 is None:
        pi0 = 1.0
    elif pi0 is not None:
        pi0 = pi0
    else:
        # evaluate pi0 for different lambdas
        pi0 = []
        lam = sp.arange(0, 0.90, 0.01)
        counts = sp.array([(pv > i).sum() for i in sp.arange(0, 0.9, 0.01)])
        for l in range(len(lam)):
            pi0.append(counts[l]/(m*(1-lam[l])))

        pi0 = sp.array(pi0)

        # fit natural cubic spline
        tck = interpolate.splrep(lam, pi0, k=3)
        pi0 = interpolate.splev(lam[-1], tck)
        if verbose:
            print("qvalues pi0=%.3f, estimated proportion of null features " % pi0)

        if pi0 > 1:
            if verbose:
                print("got pi0 > 1 (%.3f) while estimating qvalues, setting it to 1" % pi0)
            pi0 = 1.0

    assert(pi0 >= 0 and pi0 <= 1), "pi0 is not between 0 and 1: %f" % pi0

    if lowmem:
        # low memory version, only uses 1 pv and 1 qv matrices
        qv = sp.zeros((len(pv),))
        last_pv = pv.argmax()
        qv[last_pv] = (pi0*pv[last_pv]*m)/float(m)
        pv[last_pv] = -sp.inf
        prev_qv = last_pv
        for i in xrange(int(len(pv))-2, -1, -1):
            cur_max = pv.argmax()
            qv_i = (pi0*m*pv[cur_max]/float(i+1))
            pv[cur_max] = -sp.inf
            qv_i1 = prev_qv
            qv[cur_max] = min(qv_i, qv_i1)
            prev_qv = qv[cur_max]

    else:
        p_ordered = sp.argsort(pv)
        pv = pv[p_ordered]
        qv = pi0 * m/len(pv) * pv
        qv[-1] = min(qv[-1], 1.0)

        for i in xrange(len(pv)-2, -1, -1):
            qv[i] = min(pi0*m*pv[i]/(i+1.0), qv[i+1])

        # reorder qvalues
        qv_temp = qv.copy()
        qv = sp.zeros_like(qv)
        qv[p_ordered] = qv_temp

    # reshape qvalues
    qv = qv.reshape(original_shape)

    return qv
