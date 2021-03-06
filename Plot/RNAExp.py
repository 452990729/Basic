#!/usr/bin/env python

import sys
import re
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd
from scipy import stats

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=None)
    return pd_data

def MakePlot(pd_data, regress, diag, xlim, ylim):
    pd_up = pd_data[pd_data['Fc']>=0.58]
    pd_down = pd_data[pd_data['Fc']<=-0.58]
    pd_norm = pd_data[abs(pd_data['Fc'])<0.58]
    plt.style.use('my-paper')
    fig, axe = plt.subplots(figsize=(12,10))
    axe.scatter(np.log10(pd_up.iloc[:, 0]), np.log10(pd_up.iloc[:, 1]), alpha=0.8, s=100, color='r', label='UP: '+str(pd_up.shape[0]))
    axe.scatter(np.log10(pd_down.iloc[:, 0]), np.log10(pd_down.iloc[:, 1]), alpha=0.8, s=100, color='b', label='Down: '+str(pd_down.shape[0]))
    axe.scatter(np.log10(pd_norm.iloc[:, 0]), np.log10(pd_norm.iloc[:, 1]), alpha=0.8, s=100, color='black', label='Normal: '+str(pd_norm.shape[0]))
    if regress:
        slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(x), y)
        axe.annotate('$R^{2}$ = '+str(round(r_value**2, 3)), (1.05*x.min(),0.9*y.max()), size=15)
        m, b = np.polyfit(x, y, 1)
        axe.plot(x, m*x + b)
    axe.set_xlabel(pd_data.columns[0], size=30)
    axe.set_ylabel(pd_data.columns[1], size=30)
    if xlim:
        min_v, max_v=[float(i) for i in re.split(':', xlim)]
        axe.set_xlim(min_v, max_v)
    if ylim:
        min_v, max_v=[float(i) for i in re.split(':', ylim)]
        axe.set_ylim(min_v, max_v)
    if diag:
        axe.plot(axe.get_xlim(), axe.get_ylim(), ls="--", c="r", linewidth=4)
    plt.xticks(size=30)
    plt.yticks(size=30)
    plt.legend(loc=4)
    plt.savefig('ScatterPlot.pdf', dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make Scatter plot")
    parser.add_argument('-m', help='input matrix, two columns as x and y, has column name as plot label', required=True)
    parser.add_argument('-r', help='whethe plot regression line', action='store_true')
    parser.add_argument('-diag', help='whethe plot diag line', action='store_true')
    parser.add_argument('-xlim', help='the ylim of boxplot , min:max', default='')
    parser.add_argument('-ylim', help='the ylim of boxplot , min:max', default='')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    MakePlot(pd_data, argv['r'], argv['diag'], argv['xlim'], argv['ylim'])


if __name__ == '__main__':
    main()
