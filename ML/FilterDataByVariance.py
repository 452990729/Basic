#!/usr/bin/env python2

import sys
import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.feature_selection import VarianceThreshold


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def PlotVar(pd_var):
    plt.style.use('my-paper')
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(pd_var, 100)
    ax.set_xlabel('Variance')
    ax.set_ylabel('Frequency')
    plt.savefig('FeatureVariancePlot.pdf')

def VarianceThresholdSelector(data, threshold=0.5):
    selector = VarianceThreshold(threshold)
    selector.fit(data)
    return data[data.columns[selector.get_support(indices=True)]]

def main():
    pd_data = ReadData(sys.argv[1])
    pd_var = pd_data.var()
    pd_var.to_csv('Variance.txt', sep='\t', header=True, index=True)
    PlotVar(pd_var)
    if len(sys.argv) == 3:
        Y = ReadData(sys.argv[2])
        Y_list = list(np.array(Y.T)[0])
        Y_list_uniq = list(set(Y_list))
        P = round(float(Y_list.count(Y_list_uniq[0]))/len(Y_list), 2)
#        threshold = P*(1-P)
        threshold = 0.01
    else:
        threshold = 0.01
    VarianceThresholdSelector(pd_data, threshold).to_csv('FeatureFilterByVariance.txt',\
                                             sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
