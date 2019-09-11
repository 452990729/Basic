#!/usr/bin/env python2

import sys
import re
import argparse
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=None)
    return pd_data

def PlotAll(pd_data, ylim, figsize, title, out):
    plt.style.use(['my-paper', 'my-line'])
    figsize = [int(i) for i in re.split(':', figsize)]
    cols = list(pd_data.columns)
    x = pd_data.columns[0]
    y = pd_data.columns[1]
    fig, axe = plt.subplots(figsize=(figsize[0], figsize[1]))
    if len(cols) == 2:
        sns.lineplot(x=x, y=y, data=pd_data)
    elif len(cols) == 3:
        if 'hue' in cols:
            sns.lineplot(x=x, y=y, data=pd_data, hue='hue')
    plt.setp(axe.spines.values(), linewidth=3)
    axe.xaxis.set_tick_params(width=0, length=0)
    axe.xaxis.set_ticklabels([])
    axe.yaxis.set_tick_params(width=3, length=10)
    axe.set_title(title, size=30)
    if ylim:
        min_v, max_v=[int(i) for i in re.split(':', ylim)]
    else:
        min_v = pd_data.iloc[:,1].min()*0.6
        max_v = pd_data.iloc[:,1].max()*1.2
    axe.set_ylim(min_v, max_v)
    axe.set_xlabel(x, size = 40)
    axe.set_ylabel(y, size = 40)
    axe.set_yticks(axe.get_yticks()[1:-1])
    axe.set_title(title, size=30)
    plt.xticks(size = 30)
    plt.yticks(size = 30)
    plt.savefig('{}.pdf'.format(out), dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make lineplot")
    parser.add_argument('-i', help='input matrix col 0 is x, col 1 is value, col hug', required=True)
    parser.add_argument('-title', help='th title of barplot<<>>', default='')
    parser.add_argument('-ylim', help='the ylim of barplot , min:max<<>>', default='')
    parser.add_argument('-figsize', help='the figsize of barplot , width:height<<12:10>>', default='12:10')
    parser.add_argument('-o', help='the output of barplot<<BarPlot>>', default='BarPlot')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['i'])
    PlotAll(pd_data, argv['ylim'], argv['figsize'], argv['title'], argv['o'])


if __name__ == '__main__':
    main()

