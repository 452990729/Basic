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

def MakePlot(pd_data, title, xlabel, ylabel, swarm, ylim):
    plt.style.use(['my-paper', 'my-box'])
    fig, axe = plt.subplots(figsize=(20, 16))
    cols = list(pd_data.columns)
    if len(cols) == 2:
        sns.boxplot(x='Key', y='Value', data=pd_data)
        if swarm:
            sns.swarmplot(x='Key', y='Value', data=pd_data)
    elif len(cols) == 3:
        sns.boxplot(x='Key', y='Value', hue=cols[-1], data=pd_data)
        if swarm:
            sns.swarmplot(x='Key', y='Value', hue=cols[-1], data=pd_data)
    axe.set_title(title)
    if ylim:
        min_v, max_v=[float(i) for i in re.split(':', ylim)]
    else:
        min_v = pd_data.loc[:,'Value'].min()*0.6
        max_v = pd_data.loc[:,'Value'].max()*1.2
    axe.set_ylim(min_v, max_v)
    axe.set_yticks(axe.get_yticks()[1:-1])
    axe.set_xlabel(xlabel)
    axe.set_ylabel(ylabel)
    plt.xticks(rotation=40)
    plt.savefig('Boxplot.pdf', dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make boxplot")
    parser.add_argument('-i', help='input matrix col key is x, col y is value, hug is third col', required=True)
    parser.add_argument('-title', help='th title of boxplot', default='')
    parser.add_argument('-xlabel', help='the xlable of boxplot', default='')
    parser.add_argument('-ylabel', help='the ylable of boxplot', default='')
    parser.add_argument('-ylim', help='the ylim of boxplot , min,max', default='')
    parser.add_argument('-swarm', help='plot swarm', action='store_true')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['i'])
    MakePlot(pd_data, argv['title'], argv['xlabel'], argv['ylabel'], argv['swarm'], argv['ylim'])


if __name__ == '__main__':
    main()
