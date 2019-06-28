#!/usr/bin/env python

import sys
import re
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from matplotlib import pyplot as plt

def GetGene(file_in):
    list_data = []
    dict_data = {}
    with open(file_in, 'r') as f:
        for line in f:
            list_split = re.split('\t', line.strip())
            dict_data[list_split[0]] = np.array([float(i) for i in list_split[1:]])
    return dict_data

def GetTtest(list_data):
    for i in range(len(list_data)):
        for m in list_data[i+1:]:
            s, p = ttest_ind(list_data[i], m)
            print p

def MakePlot(dict_data, title, xlabel, ylabel):
    plt.style.use(['my-paper', 'my-box'])
    fig, axe = plt.subplots(figsize=(16, 16))
    keys = sorted(dict_data.keys())
    list_data = [dict_data[i] for i in keys]
    axe.boxplot(list_data, positions= range(len(list_data,)))
    sns.swarmplot(data=list_data)

    axe.set_title(title)
    min_v = min([np.min(i) for i in list_data])
    max_v = max([np.max(i) for i in list_data])
    axe.set_ylim(min_v*0.6, max_v*1.2)
    axe.set_yticks(axe.get_yticks()[1:-1])
    axe.set_xlabel(xlabel)
    axe.set_ylabel(ylabel)
    plt.xticks(rotation=40)
    plt.setp(axe, xticks=range(len(list_data,)), xticklabels= keys)
    plt.savefig('Boxplot.pdf', dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make boxplot")
    parser.add_argument('-i', help='input file, one line one box, seprate by \\t, first col is lable', required=True)
    parser.add_argument('-title', help='th title of boxplot', default='')
    parser.add_argument('-xlabel', help='the xlable of boxplot', default='')
    parser.add_argument('-ylabel', help='the ylable of boxplot', default='')
    argv=vars(parser.parse_args())
    dict_data = GetGene(argv['i'])
    MakePlot(dict_data, argv['title'], argv['xlabel'], argv['ylabel'])


if __name__ == '__main__':
    main()
