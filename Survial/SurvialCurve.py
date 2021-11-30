#!/usr/bin/env python2

import sys
import re
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from copy import deepcopy
from matplotlib import pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test


def HandleSurvalData(file_in, trim):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    pd_out = pd_data.loc[:, ['OS', 'status']]
    if pd_out['OS'].median(0) > 200:
        label = 'days'
        if trim:
            pd_out.loc[pd_out.OS>trim, ['OS', 'status']] = trim,0
    else:
        label = 'months'
    return pd_out, label

def HandleClassData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def CalPairPvalue(pd1, pd2):
    results = logrank_test(pd1['OS'], pd2['OS'],\
                          event_observed_A=pd1['status'], event_observed_B=pd2['status'])
    p_value = results.p_value
    if p_value <= 0.001:
#        return '***'
        return 'p < 0.001'
    elif p_value <= 0.01:
#        return '**'
        return str(round(p_value, 3))
    elif p_value <= 0.05:
        return str(round(p_value, 2))
    else:
#        return str(round(p_value, 2))
#        return 'n.s.'
        return str(round(p_value, 2))
#        return str(0.05)

def MakePlot(pd_surval, lb, time_label, pd_class=False):
    plt.style.use(['my-paper', 'my-line'])
    fig, axe = plt.subplots(figsize=(10,8))
    kmf = KaplanMeierFitter()
    if type(pd_class) != 'bool':
        Cluster = list(set(list(np.array(pd_class.T)[0])))
        dict_tmp = {}
        for cls in Cluster:
            index = pd_class[pd_class.iloc[:,0]==cls].index
            pd_Data = pd_surval.loc[index, :]
            pd_Data.drop(pd_Data[np.isnan(pd_Data['OS'])].index, inplace=True)
            pd_Data = pd_Data.dropna(axis=0,how='any')
            dict_tmp[cls] = deepcopy(pd_Data)
            kmf.fit(pd_Data['OS'], pd_Data['status'], label=cls)
            kmf.plot(ax=axe, ci_show=False)
        P_lable = ''
        for i in range(len(Cluster)-1):
            for value in Cluster[i+1:]:
                p_value = CalPairPvalue(dict_tmp[Cluster[i]], dict_tmp[value])
                P_lable += '{} VS {}: {}\n'.format(Cluster[i], value, p_value)
        if P_lable.count('VS') == 1:
            P_lable = 'log rank p: '+re.split(':', P_lable)[1]
        axe.plot([], [], ' ', label=P_lable)
        plt.legend(loc='lower left')
    else:
        kmf.fit(pd_surval['OS'], pd_surval['status'])
        kmf.plot(ax=axe, ci_show=False)
    axe.set_ylim(0, 1)
    axe.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    axe.set_ylabel('Survival Probability')
    axe.set_xlabel('Time ({})'.format(time_label))
    axe.set_title(lb)
    plt.savefig('{}SurvalPlot.pdf'.format(lb))

def main():
    parser = argparse.ArgumentParser(description="Surval curve")
    parser.add_argument('-s', help='input surval file ,include OS and status columns', required=True)
    parser.add_argument('-c', help='cluster file, two lines, label and cluster', default=None)
    parser.add_argument('-t', help='the title of the plot <<>>', default='')
    parser.add_argument('-trim', help='trim time to cutoff <<>>', type=int, default=1825)
    argv=vars(parser.parse_args())
    pd_surval, time_label = HandleSurvalData(argv['s'], argv['trim'])
    if argv['c']:
        pd_class = HandleClassData(argv['c'])
        MakePlot(pd_surval, argv['t'], time_label, pd_class)
    else:
        MakePlot(pd_surval, argv['t'], time_label)


if __name__ == '__main__':
    main()
