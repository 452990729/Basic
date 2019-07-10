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


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=None)
    return pd_data

def MakePlot(pd_data):
    plt.style.use('my-paper')
    fig, axScatter = plt.subplots(figsize=(8, 8))
    x = pd_data.iloc[:,0]
    y = pd_data.iloc[:,1]
    axScatter.scatter(x, y)
    divider = make_axes_locatable(axScatter)
    axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=axScatter)
    axHisty = divider.append_axes("right", 1.2, pad=0.1, sharey=axScatter)
    axHistx.xaxis.set_tick_params(labelbottom=False)
    axHisty.yaxis.set_tick_params(labelleft=False)
    binwidth = 0.25
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1)*binwidth
    bins = np.arange(-lim, lim + binwidth, binwidth)
    axHistx.hist(x, bins=bins)
    axHisty.hist(y, bins=bins, orientation='horizontal')
    axScatter.set_xlabel(pd_data.columns[0])
    axScatter.set_ylabel(pd_data.columns[1])
    for ax in [axScatter, axHistx, axHisty]:
        ax.spines['right'].set_visible(True)
        ax.spines['top'].set_visible(True)
    axHistx.tick_params(axis='x', which='both', length=0)
    axHisty.tick_params(axis='y', which='both', length=0)
    plt.savefig('ScatterHist.pdf')


def main():
    parser = argparse.ArgumentParser(description="make ScatterHist plot")
    parser.add_argument('-m', help='input matrix, two columns as x and y, has column name as plot label', required=True)
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    MakePlot(pd_data)


if __name__ == '__main__':
    main()
