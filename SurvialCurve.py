#!/usr/bin/env python2


import sys
import re
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from lifelines import KaplanMeierFitter


def HandleSurvalData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    pd_out = pd_data.loc[:, ['days_to_know', 'status']]
    return pd_out

def HandleClassData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def MakePlot(pd_surval, pd_class=False):
    plt.style.use('my-paper')
    fig, axe = plt.subplots(figsize=(10,8))
    kmf = KaplanMeierFitter()
    if type(pd_class) != 'bool':
        Cluster = set(list(np.array(pd_class.T)[0]))
        for cls in Cluster:
            index = pd_class[pd_class.iloc[:,0]==cls].index
            pd_Data = pd_surval.loc[index, :]
            pd_Data.drop(pd_Data[np.isnan(pd_Data['days_to_know'])].index, inplace=True)
            kmf.fit(pd_Data['days_to_know'], pd_Data['status'], label=cls)
            kmf.plot(ax=axe, ci_show=False)
    else:
        kmf.fit(pd_surval['days_to_know'], pd_surval['status'])
        kmf.plot(ax=axe, ci_show=False)
    plt.savefig('SurvalPlot.pdf')

def main():
    parser = argparse.ArgumentParser(description="Surval curve")
    parser.add_argument('-s', help='input surval file ,include days_to_know and status columns', required=True)
    parser.add_argument('-c', help='cluster file, two lines, label and cluster', default=None)
    argv=vars(parser.parse_args())
    pd_surval = HandleSurvalData(argv['s'])
    if argv['c']:
        pd_class = HandleClassData(argv['c'])
        MakePlot(pd_surval, pd_class)
    else:
        MakePlot(pd_surval)


if __name__ == '__main__':
    main()
