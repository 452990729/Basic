#!/usr/bin/env python
# coding: utf-8

import re
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=None)
    return pd_data

def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)

def MakePlot(pd_data, group_lb, data_lb, figsize, outfile, title, xlim):
    figsize = [int(i) for i in re.split(':', figsize)]
    fig, axe = plt.subplots(figsize=(figsize[0], figsize[1]))
    pal_len = len(set(list(np.array(pd_data.loc[:, group_lb]))))
    pal = sns.cubehelix_palette(pal_len, rot=-.25, light=.7)
    g = sns.FacetGrid(pd_data, row=group_lb, hue=group_lb, aspect=15, height=.5, palette=pal)
    g.map(sns.kdeplot, data_lb, clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
    g.map(sns.kdeplot, data_lb, clip_on=False, color="w", lw=2, bw=.2)
    g.map(plt.axhline, y=0, lw=2, clip_on=False)
    g.map(label, data_lb)
    if xlim:
        min_v, max_v=[float(i) for i in re.split(':', xlim)]
    else:
        min_v = pd_data.loc[:,data_lb].min()*0.6
        max_v = pd_data.loc[:,data_lb].max()*1.2
    g.set(xlim=[min_v, max_v])
    g.fig.subplots_adjust(hspace=-.25)
    g.set_titles(title)
    g.set(yticks=[])
    g.despine(bottom=True, left=True)
    plt.savefig(outfile, dpi=600)

def main():
    parser = argparse.ArgumentParser(description="make joyplot")
    parser.add_argument('-i', help='input matrix, col is group and value, no index ,has header', required=True)
    parser.add_argument('-g', help='the group label of input', required=True)
    parser.add_argument('-x', help='the value label of input', required=True)
    parser.add_argument('-title', help='the title of joyplot<<>>', default='')
    parser.add_argument('-xlim', help='the xlim of joyplot , min:max<<>>', default='')
    parser.add_argument('-figsize', help='the figsize of joyplot , width:height<<10:6>>', default='10:6')
    parser.add_argument('-o', help='output<<Joyplot.pdf>>', default='Joyplot.pdf')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['i'])
    MakePlot(pd_data, argv['g'], argv['x'], argv['figsize'], argv['o'], argv['title'], argv['xlim'])

if __name__ == '__main__':
	main()
