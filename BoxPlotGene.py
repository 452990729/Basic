#!/usr/bin/env python

import sys
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind
from scipy.stats import ranksums
from scipy.stats.mstats import kruskalwallis
from scipy.stats import ks_2samp
def GetGene(file_in, tp):
    list_data = []
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_split = re.split('\t', line.strip())
            if list_split[0] == tp:
                np1 = np.array([float(i) for i in list_split[1:9]])
                np2 = np.array([float(i) for i in list_split[9:16]])
                np3 = np.array([float(i) for i in list_split[16:]])
                list_data = [np1, np2, np3]
    return list_data

def GetTtest(list_data):
    for i in range(len(list_data)):
        for m in list_data[i+1:]:
            s, p = ttest_ind(list_data[i], m)
            print p

def MakePlot(list_data, tp):
    fig, axe = plt.subplots(figsize=(6,8))
    boxprops = dict(linewidth=3)
    medianprops = dict(linewidth=3)
    whiskerprops = dict(linewidth=2)
    capprops = dict(linewidth=2)
    axe.boxplot(list_data, showfliers=False, widths=0.6, boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops)
    axe.set_title(tp+' Expression', size=20)
    axe.set_ylim(50, 170)
    axe.set_yticks([60,80,100,120,140])
    plt.xticks(size = 18, rotation=20)
    plt.yticks(size = 18)
    plt.setp(axe.spines.values(), linewidth=3)
    axe.yaxis.set_tick_params(width=3, length=10)
    axe.xaxis.set_tick_params(width=3, length=10)
#    axe.set_aspect(0.003)
    axe.spines['right'].set_visible(False)
    axe.spines['top'].set_visible(False)
    plt.setp(axe, xticks=[y + 1 for y in range(len(list_data,))],\
                      xticklabels=['normal', 'psoriatic', 'uninvolved'])
    plt.savefig('{}.pdf'.format(tp), dpi=300)

def main():
    list_data = GetGene(sys.argv[1], sys.argv[2])
    MakePlot(list_data, sys.argv[2])
    GetTtest(list_data)


if __name__ == '__main__':
    main()



