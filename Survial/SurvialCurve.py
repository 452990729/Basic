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


def HandleSurvalData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    pd_out = pd_data.loc[:, ['days_to_know', 'status']]
    if pd_out['days_to_know'].median(0) > 200:
        label = 'days'
        pd_out.loc[pd_out.days_to_know>1825, ['days_to_know', 'status']] = 1825,0
    else:
        lable = 'months'
    return pd_out, label

def HandleClassData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def CalPairPvalue(pd1, pd2):
    results = logrank_test(pd1['days_to_know'], pd2['days_to_know'],\
                          event_observed_A=pd1['status'], event_observed_B=pd2['status'])
    p_value = results.p_value
    if p_value <= 0.001:
        return '***'
    elif p_value <= 0.01:
        return '**'
    elif p_value <= 0.05:
        return '*'
    else:
#        return str(round(p_value, 2))
        return 'n.s.'

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
            pd_Data.drop(pd_Data[np.isnan(pd_Data['days_to_know'])].index, inplace=True)
            dict_tmp[cls] = deepcopy(pd_Data)
            kmf.fit(pd_Data['days_to_know'], pd_Data['status'], label=cls)
            kmf.plot(ax=axe, ci_show=False)
        P_lable = ''
        for i in range(len(Cluster)-1):
            for value in Cluster[i+1:]:
                p_value = CalPairPvalue(dict_tmp[Cluster[i]], dict_tmp[value])
                P_lable += '{} VS {}: {}\n'.format(Cluster[i], value, p_value)
        if P_lable.count('VS') == 1:
            P_lable = 'log rank p: '+re.split(':', P_lable)[1]
        axe.plot([], [], ' ', label=P_lable)
        plt.legend(loc='upper right')
    else:
        kmf.fit(pd_surval['days_to_know'], pd_surval['status'])
        kmf.plot(ax=axe, ci_show=False)
    axe.set_ylim(0, 1)
    axe.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    axe.set_ylabel('Survival Probability')
    axe.set_xlabel('Time ({})'.format(time_label))
    axe.set_title(lb)
    plt.savefig('{}SurvalPlot.pdf'.format(lb))

def main():
    parser = argparse.ArgumentParser(description="Surval curve")
    parser.add_argument('-s', help='input surval file ,include days_to_know and status columns', required=True)
    parser.add_argument('-c', help='cluster file, two lines, label and cluster', default=None)
    parser.add_argument('-t', help='the title of the plot', default='')
    argv=vars(parser.parse_args())
    pd_surval, time_label = HandleSurvalData(argv['s'])
    if argv['c']:
        pd_class = HandleClassData(argv['c'])
        MakePlot(pd_surval, argv['t'], time_label, pd_class)
    else:
        MakePlot(pd_surval, argv['t'], time_label)


if __name__ == '__main__':
    main()
