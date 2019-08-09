#!/usr/bin/env python2


import sys
import re
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from copy import deepcopy
from matplotlib import pyplot as plt
from lifelines import CoxPHFitter


def HandleSurvalData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    pd_out = pd_data.loc[:, ['OS', 'status']]
    return pd_out

def HandleVarData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def CoxAnalysis(pd_data, pd_surval, tp):
    cph = CoxPHFitter(penalizer=0.1)
    if tp == 'univariate':
        pd_out = ''
        for i in range(pd_data.shape[1]):
            df = pd_surval.T.append(pd_data.iloc[:,i].T).T
            cph.fit(df, 'OS', event_col='status', step_size=0.1)
            if type(pd_out) == str:
                pd_out = cph.summary
            else:
                pd_out=pd_out.append(cph.summary)
    elif tp == 'multivariable':
        df = pd_data.T.append(pd_surval.T).T
        cph.fit(df, 'OS', event_col='status', step_size=0.1)
        pd_out = cph.summary
    pd_out.to_csv('CoxRegress.txt', sep='\t', header=True, index=True)
    plt.style.use('my-paper')
    fig, axe = plt.subplots(figsize=(25,8))
    cph.plot(ax=axe)
    axe.set_ylim(-0.2,3.2)
    axe.set_xlim(-2.5,2.1)
    plt.savefig('CoxRegress.pdf')

def main():
    parser = argparse.ArgumentParser(description="Cox regression")
    parser.add_argument('-s', help='input surval file ,include OS and status columns', required=True)
    parser.add_argument('-c', help='var matrix, var in the columns', required=True)
    parser.add_argument('-t', help='univariate or multivariable<univariate>>', choices=['univariate', 'multivariable'], default='univariate')
    argv=vars(parser.parse_args())
    pd_surval = HandleSurvalData(argv['s'])
    pd_data = HandleVarData(argv['c'])
    pd_surval = pd_surval.loc[pd_data.index,:]
    CoxAnalysis(pd_data, pd_surval, argv['t'])


if __name__ == '__main__':
    main()
