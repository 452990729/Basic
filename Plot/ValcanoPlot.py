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
    pd_data = pd_data[pd_data['log2FoldChange'].notnull()]
    pd_data = pd_data[pd_data['padj'].notnull()]
    return pd_data

def MakePlot(pd_data, fdr, fold, xlim, ylim):
    up = pd_data[(pd_data['padj'] < fdr)&(pd_data['log2FoldChange'] > np.log2(fold))]
    up.loc[:, 'padj'] = np.abs(np.log10(up['padj']))
    down = pd_data[(pd_data['padj'] < fdr)&(pd_data['log2FoldChange'] < float('-'+str(np.log2(fold))))]
    down.loc[:, 'padj'] = np.abs(np.log10(down['padj']))
    normal = pd_data[(pd_data['padj'] >= fdr)|(abs(pd_data['log2FoldChange']) <= np.log2(fold))]
    normal.loc[:, 'padj'] = np.abs(np.log10(normal['padj']))
    plt.style.use('my-paper')
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.scatter(up['log2FoldChange'], up['padj'], c='#A52A2A', marker='o', alpha=1, edgecolors='none', label='Up: '+str(up.shape[0]))
    ax.scatter(down['log2FoldChange'], down['padj'], c='#6495ED', marker='o', alpha=1, edgecolors='none', label='Down: '+str(down.shape[0]))
    ax.scatter(normal['log2FoldChange'], normal['padj'], c='#D3D3D3', marker='o', alpha=1, edgecolors='none', label='Normal: '+str(normal.shape[0]))
    ax.set_xlabel('logFC')
    ax.set_ylabel('-log10(Pvalue)')
    [xmin, xmax] = [float(i) for i in re.split(':', xlim)]
    ax.set_xlim(xmin, xmax)
    [ymin, ymax] = [float(i) for i in re.split(':', ylim)]
#    ax.set_yticks([0, 5, 10, 15])
    ax.set_ylim(ymin, ymax)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    plt.savefig('Valcano.pdf')

def main():
    parser = argparse.ArgumentParser(description="Valcano Plot")
    parser.add_argument('-m', help='input expression matrix, must contain log2FoldChange and padj columns', required=True)
    parser.add_argument('-p', help='fdr cutoff <<0.05>>', default=0.05)
    parser.add_argument('-xlim', help='fdr cutoff <<-10:10>>', default='-10:10')
    parser.add_argument('-ylim', help='fdr cutoff <<-0.5:10>>', default='-0.5:10')
    parser.add_argument('-f', help='FoldChange cutoff <<1>>', default=1)
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    MakePlot(pd_data, argv['p'], float(argv['f']), argv['xlim'], argv['ylim'])


if __name__ == '__main__':
    main()

