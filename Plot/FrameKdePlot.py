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

def PlotAll(pd_data, x, y, hue, ylim, figsize, outfile):
    plt.style.use(['my-paper', 'my-line'])
    figsize = [int(i) for i in re.split(':', figsize)]
    fig, axe = plt.subplots(figsize=(figsize[0], figsize[1]))
    if hue:
        if x:
            sns.kdeplot(data=pd_data, x=x, hue=hue,)
        elif y:
            sns.kdeplot(data=pd_data, y=y, hue=hue,)
    else:
        if x:
            sns.kdefplot(data=pd_data, x=x, )
        elif y:
            sns.kdefplot(data=pd_data, y=y, )
    plt.setp(axe.spines.values(), linewidth=3)
    axe.xaxis.set_tick_params(width=0, length=0)
#    axe.xaxis.set_ticklabels([])
    axe.yaxis.set_tick_params(width=3, length=10)
    if ylim:
        min_v, max_v=[int(i) for i in re.split(':', ylim)]
        axe.set_ylim(min_v, max_v)
    axe.set_xlabel(x, size = 40)
    axe.set_ylabel(y, size = 40)
    axe.set_yticks(axe.get_yticks()[1:])
    plt.xticks(size = 30)
    plt.yticks(size = 30)
#    axe.legend(loc='lower right')
    plt.savefig(outfile, dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make lineplot")
    parser.add_argument('-i', help='input matrix col x, y, hug', required=True)
    parser.add_argument('-ylim', help='the ylim of barplot , min:max<<>>', default='')
    parser.add_argument('-figsize', help='the figsize of barplot , width:height<<12:10>>', default='12:10')
    parser.add_argument('-x', help='the x of plot<<>>', default='')
    parser.add_argument('-y', help='the y of plot<<>>', default='')
    parser.add_argument('-hue', help='the huge of plot<<>>', default='')
    parser.add_argument('-o', help='the output of barplot<<KdePlot.pdf>>', default='KdePlot.pdf')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['i'])
    PlotAll(pd_data, argv['x'], argv['y'], argv['hue'], argv['ylim'], argv['figsize'], argv['o'])


if __name__ == '__main__':
    main()

