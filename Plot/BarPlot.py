#!/usr/bin/env python2


import sys
import re
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def MakePlot(pd_data, tp, title, xlabel, ylabel, size, out):
    plt.style.use('my-paper')
    list_size = re.split(',', size)
    fig, ax = plt.subplots(figsize=(int(list_size[0]),int(list_size[1])))
    list_bar = []
    x = np.arange(pd_data.shape[0])
    if tp == 'stack':
        width = 0.8
        for i in range(pd_data.shape[1]):
            list_bar.append('p'+str(i))
            if i == 0:
                locals()['p'+str(i)] = plt.bar(x, pd_data.iloc[:, i], width)
            else:
                locals()['p'+str(i)] = plt.bar(x, pd_data.iloc[:, i], width, bottom=pd_data.iloc[:, i-1])
        ax.set_xticks(x)
    elif tp == 'group':
        width = 0.8/pd_data.shape[1]
        for i in range(pd_data.shape[1]):
            list_bar.append('p'+str(i))
            locals()['p'+str(i)] = plt.bar(x+width*i, pd_data.iloc[:, i], width)
        ax.set_xticks(x+width*(pd_data.shape[1]-1))
    ax.set_xticklabels(list(pd_data.index), rotation=45)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if pd_data.shape[0] > 1:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend([locals()[m][0] for m in list_bar], list(pd_data.columns),\
                 loc='upper left', bbox_to_anchor=(1, 0.5), frameon=False)
    plt.savefig('{}.pdf'.format(out), dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make barplot")
    parser.add_argument('-m', help='input matrix, index are xlabel, columns are class', required=True)
    parser.add_argument('-type', help='th type of barplot <<stack>>', choices=['stack', 'group'], default='stack')
    parser.add_argument('-title', help='th title of boxplot', default='')
    parser.add_argument('-xlabel', help='the xlable of boxplot', default='')
    parser.add_argument('-ylabel', help='the ylable of boxplot', default='')
    parser.add_argument('-size', help='the figsize of boxplot, width,height, <<10,15>>', default='10,15')
    parser.add_argument('-out', help='the output of boxplot', default='Barplot')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    MakePlot(pd_data, argv['type'], argv['title'], argv['xlabel'], argv['ylabel'], argv['size'], argv['out'])


if __name__ == '__main__':
    main()
