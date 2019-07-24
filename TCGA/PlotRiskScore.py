#!/usr/bin/env python2


import sys
import re
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as mpatches
import seaborn as sns

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def GetRank(pd_data, lb):
    pd_sort = pd_data.sort_values(lb)
    return pd_sort

def PlotScatter(pd_data, pd_surv, ax):
    x = range(pd_data.shape[0])
    y = pd_surv.loc[:, 'OS'].loc[pd_data.index]
    shape = pd_surv.loc[:, 'status'].loc[pd_data.index]
    m = 0
    n = 0
    patches  = []
    for i in range(shape.shape[0]):
        if shape[i] == 0:
            marker = 'o'
            ci = 'g'
            ps = ax.scatter(x[i], y[i], marker=marker, color=ci, label='Alive')
            if m == 0:
                patches.append(ps)
                m += 1
        elif shape[i] == 1:
            marker = '^'
            ci = 'r'
            ps = ax.scatter(x[i], y[i], marker=marker, color=ci, label='Dead')
            if n == 0:
                patches.append(ps)
                n += 1
    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_visible(True)
    ax.set_ylabel('Overall survival(days)')
    ax.set_xlim(-5, max(x)+5)
    ax.set_ylim(-100, y.max()+5)
    ax.set_xticks(range(0, max(x)+5, 100))
    ax.set_yticks(range(0, int(y.max())+5, 1000))
    x_mean = [np.mean(x)]*y.shape[0]
    ax.plot(x_mean, y, linestyle='--', linewidth=3)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(handles=patches, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

def PlotLine(pd_data, ax):
    x = range(pd_data.shape[0])
    y = pd_data.iloc[:,0]
    ax.plot(x, y, 'r-', lw=2)
    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_visible(True)
    ax.set_ylabel('Risk score')
    ax.tick_params(axis='x', which='both', length=0)
    ax.tick_params(axis='y', which='both', length=0)
    ax.set_xlim(-5, max(x)+5)
    ax.set_ylim(y.min()-1, int(y.max())+1)
    x_mean = [np.mean(x)]*pd_data.shape[0]
    ax.plot(x_mean, pd_data.iloc[:,0], linestyle='--', linewidth=3)
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)

def PlotHeatmap(pd_data, pd_gene, fig, ax):
    means = pd_data.shape[0]/2
    list_hl = ['Low' if i<=means else 'High' for i in range(pd_data.shape[0])]
    pd_data['Level'] = list_hl
    pd_gene = pd_gene.loc[:, pd_data.index]
#    for index in list(pd_gene.index):
#        pd_gene.loc[index,:] = (pd_gene.loc[index,:] - pd_gene.loc[index,:].mean())/pd_gene.loc[index,:].std(ddof=0)
    for col in list(pd_gene.columns):
        pd_gene[col] = (pd_gene[col] - pd_gene[col].mean())/pd_gene[col].std(ddof=0)
    cbar_ax = fig.add_axes([.78, .13, .015, .25])
    hp = sns.heatmap(pd_gene, xticklabels=False ,ax=ax, cmap="bwr", cbar=1, cbar_ax=cbar_ax)
    ax.tick_params(axis='y', which='both', length=0)

def PlotBar(pd_data, ax):
    means = pd_data.shape[0]/2
    ax.barh([1,], [means,], height=0.1, color='b')
    ax.barh([1,], [pd_data.shape[0]-means,], height=0.1, left=means, color='r')
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)
    ax.tick_params(axis='x', which='both', length=0)
    ax.tick_params(axis='y', which='both', length=0)

def MakePlot(pd_data, pd_surv, pd_gene):
    plt.style.use(['my-paper', 'my-line'])
    fig, ax = plt.subplots(figsize=(15, 12))
    divider = make_axes_locatable(ax)
    PlotScatter(pd_data, pd_surv, ax)
    ax_line = divider.append_axes("top", 2, pad=0.1, sharex=ax)
    PlotLine(pd_data, ax_line)
    ax_heatmap = divider.append_axes("bottom", 3, pad=0.1, sharex=ax)
    PlotHeatmap(pd_data, pd_gene, fig, ax_heatmap)
    ax_bar = divider.append_axes("bottom", 0.3, pad=0.1, sharex=ax)
    PlotBar(pd_data, ax_bar)
    plt.savefig('RiskScore.pdf')

def main():
    parser = argparse.ArgumentParser(description="make RiskScore plot")
    parser.add_argument('-r', help='input risk score matrix, include header and index', required=True)
    parser.add_argument('-s', help='input survival matrix, include header and index, include OS and status columns', required=True)
    parser.add_argument('-e', help='input exp matrix, include header and index', required=True)
    parser.add_argument('-l', help='input risk score matrix risk score column name<<RiskScore>>', default='RiskScore')
    argv=vars(parser.parse_args())
    pd_r = ReadData(argv['r'])
    pd_s = ReadData(argv['s'])
    pd_e = ReadData(argv['e'])
    pd_sort = GetRank(pd_r, argv['l'])
    MakePlot(pd_sort, pd_s, pd_e.T)


if __name__ == '__main__':
    main()
