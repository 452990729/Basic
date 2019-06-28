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
    pd_out = pd_data.loc[:, ['days_to_know', 'status']]
    return pd_out

def HandleVarData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def CoxAnalysis(df):
    cph = CoxPHFitter(penalizer=0.1)
    cph.fit(df, 'days_to_know', event_col='status')
    pd_out = cph.summary
    pd_out.to_csv('CoxRegress.txt', sep='\t', header=True, index=True)
    plt.style.use('my-paper')
    fig, axe = plt.subplots(figsize=(10,8))
    cph.plot(ax=axe)
    plt.savefig('CoxRegress.pdf')

def main():
    parser = argparse.ArgumentParser(description="Cox regression")
    parser.add_argument('-s', help='input surval file ,include days_to_know and status columns', required=True)
    parser.add_argument('-c', help='var matrix, var in the columns', required=True)
    argv=vars(parser.parse_args())
    pd_surval = HandleSurvalData(argv['s'])
    pd_data = HandleVarData(argv['c'])
    df = pd_data.T.append(pd_surval.T).T
    df.drop(df[np.isnan(df['days_to_know'])].index, inplace=True)
    CoxAnalysis(df)


if __name__ == '__main__':
    main()
