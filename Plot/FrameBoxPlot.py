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
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=None)
    return pd_data


def GetTtest(list_data):
    for i in range(len(list_data)):
        for m in list_data[i+1:]:
            s, p = ttest_ind(list_data[i], m)
            print p

def MakePlot(pd_data, title, xlabel, ylabel, x, y, huge, swarm, violin, ylim, figsize, outfile):
    plt.style.use(['my-paper', 'my-box'])
    figsize = [int(i) for i in re.split(':', figsize)]
    fig, axe = plt.subplots(figsize=(figsize[0], figsize[1]))
    boxprops = dict(linewidth=4)
    medianprops = dict(linewidth=6)
    whiskerprops = dict(linewidth=4)
    capprops = dict(linewidth=4)
    if swarm:
        sns.boxplot(x=swarm, y=y, data=pd_data, boxprops=boxprops,
                    medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops)
        sns.swarmplot(x=swarm, y=y, data=pd_data, size=10)
    elif violin:
        sns.violinplot(x=violin, y=y, data=pd_data)
    elif huge:
        sns.boxplot(x=x, y=y, hue=huge, data=pd_data, boxprops=boxprops,
                    medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops)
    else:
        sns.boxplot(x=x, y=y, data=pd_data, boxprops=boxprops,
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
        min_v = pd_data.loc[:,y].min()*0.6
        max_v = pd_data.loc[:,y].max()*1.2
    axe.set_ylim(min_v, max_v)
    axe.set_yticks(axe.get_yticks()[1:-1])
    axe.set_xlabel(xlabel, size = 40)
    axe.set_ylabel(ylabel, size = 40)
#    plt.xticks(size = 30, rotation=40)
    plt.xticks(size = 30)
    plt.yticks(size = 30)
    plt.savefig(outfile, dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make boxplot")
    parser.add_argument('-i', help='input matrix col key is x, col y is value, hug is third col', required=True)
    parser.add_argument('-title', help='th title of boxplot<<>>', default='')
    parser.add_argument('-xlabel', help='the xlable of boxplot<<>>', default='')
    parser.add_argument('-ylabel', help='the ylable of boxplot<<>>', default='')
    parser.add_argument('-x', help='the x of box<<>>', default='')
    parser.add_argument('-y', help='the y of box<<>>', default='')
    parser.add_argument('-huge', help='the huge of box<<>>', default='')
    parser.add_argument('-ylim', help='the ylim of boxplot , min:max<<>>', default='')
    parser.add_argument('-figsize', help='the figsize of boxplot , width:height<<6:15>>', default='6:15')
    parser.add_argument('-swarm', help='plot swarm <<>>', default='')
    parser.add_argument('-violin', help='plot violin <<>>', default='')
    parser.add_argument('-o', help='output<<Boxplot.pdf>>', default='Boxplot.pdf')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['i'])
    MakePlot(pd_data, argv['title'], argv['xlabel'], argv['ylabel'], argv['x'], argv['y'], argv['huge'], argv['swarm'], argv['violin'], argv['ylim'], argv['figsize'], argv['o'])


if __name__ == '__main__':
    main()
