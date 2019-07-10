#!/usr/bin/env python

import sys
import re
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy import stats

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index=None)
    return pd_data

def MakePlot(pd_data):
    x = pd_data.iloc[:, 0]
    y = pd_data.iloc[:, 1]
    plt.style.use('my-paper')
    fig, ax = plt.subplots()
    colors = np.random.rand(len(x))
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(x), y)
    ax.scatter(x, y, alpha=0.5)
    ax.annotate('$R^{2}$ = '+str(round(r_value**2, 3)), (1.05*x.min(),0.9*y.max()), size=15)
    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x + b)
    ax.set_xlabel(pd_data.columns[0])
    ax.set_ylabel(pd_data.columns[1])
    plt.savefig('ScatterPlot.pdf', dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make Scatter plot")
    parser.add_argument('-m', help='input matrix, two columns as x and y, has column name as plot label', required=True)
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    MakePlot(pd_data)


if __name__ == '__main__':
    main()
