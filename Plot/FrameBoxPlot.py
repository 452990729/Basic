#!/usr/bin/env python

import sys
import re
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from matplotlib import pyplot as plt

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data


def GetTtest(list_data):
    for i in range(len(list_data)):
        for m in list_data[i+1:]:
            s, p = ttest_ind(list_data[i], m)
            print p

def MakePlot(pd_data, title, xlabel, ylabel, swarm, violin, ylim, figsize):
    plt.style.use(['my-paper', 'my-box'])
    figsize = [int(i) for i in re.split(':', figsize)]
    fig, axe = plt.subplots(figsize=(figsize[0], figsize[1]))
    cols = list(pd_data.columns)
    boxprops = dict(linewidth=4)
    medianprops = dict(linewidth=6)
    whiskerprops = dict(linewidth=4)
    capprops = dict(linewidth=4)
    if len(cols) == 2:
        if swarm:
            sns.swarmplot(x='Key', y='Value', data=pd_data, size=10)
            sns.boxplot(x='Key', y='Value', data=pd_data, boxprops=boxprops,
                        medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops)
        elif violin:
            sns.violinplot(x='Key', y='Value', data=pd_data)
        else:
            sns.boxplot(x='Key', y='Value', data=pd_data, boxprops=boxprops,
                        medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops)
    elif len(cols) == 3:
        title = pd_data.iloc[0,0]
        if swarm:
            sns.boxplot(x=cols[-1], y='Value', data=pd_data, boxprops=boxprops,
                       medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops)
            sns.swarmplot(x=cols[-1], y='Value', data=pd_data, size=10)
        elif violin:
            sns.violinplot(x=cols[-1], y='Value', data=pd_data)
        else:
            sns.boxplot(x='Key', y='Value', hue=cols[-1], data=pd_data, boxprops=boxprops,
                       medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops)
    for patch in axe.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 1))
    plt.setp(axe.spines.values(), linewidth=3)
    axe.yaxis.set_tick_params(width=3, length=10)
    axe.xaxis.set_tick_params(width=3, length=10)
    axe.set_title(title, size=30)
    if ylim:
        min_v, max_v=[float(i) for i in re.split(':', ylim)]
    else:
        min_v = pd_data.loc[:,'Value'].min()*0.6
        max_v = pd_data.loc[:,'Value'].max()*1.2
    axe.set_ylim(min_v, max_v)
    axe.set_yticks(axe.get_yticks()[1:-1])
    axe.set_xlabel(xlabel)
    axe.set_ylabel(ylabel)
    plt.xticks(size = 30, rotation=40)
    plt.yticks(size = 30)
    plt.savefig('Boxplot.pdf', dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make boxplot")
    parser.add_argument('-i', help='input matrix col key is x, col y is value, hug is third col', required=True)
    parser.add_argument('-title', help='th title of boxplot', default='')
    parser.add_argument('-xlabel', help='the xlable of boxplot', default='')
    parser.add_argument('-ylabel', help='the ylable of boxplot', default='')
    parser.add_argument('-ylim', help='the ylim of boxplot , min:max', default='')
    parser.add_argument('-figsize', help='the figsize of boxplot , min:max', default='6:15')
    parser.add_argument('-swarm', help='plot swarm', action='store_true')
    parser.add_argument('-violin', help='plot violin', action='store_true')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['i'])
    MakePlot(pd_data, argv['title'], argv['xlabel'], argv['ylabel'], argv['swarm'], argv['violin'], argv['ylim'], argv['figsize'])


if __name__ == '__main__':
    main()
