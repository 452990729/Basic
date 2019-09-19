#!/usr/bin/env python2


import sys
import re
import os
import argparse
import pandas as pd
from lifelines.statistics import logrank_test


BasePath = os.path.split(os.path.realpath(__file__))[0]
SurvialCurve = BasePath+'/SurvialCurve.py'

def HandleCoxData(file_in, p):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    pd_filter = pd_data[pd_data['p']<=p]
    return list(pd_filter.index)

def HandleExpData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def CalPairPvalue(pd1, pd2):
    results = logrank_test(pd1['OS'], pd2['OS'],\
                           event_observed_A=pd1['status'], event_observed_B=pd2['status'])
    p_value = results.p_value
    return p_value

def ClassDataByMedian(pd_exp, label):
    pd_lb = pd_exp.loc[:, label]
    median = pd_lb.median()
    if median != 0:
        pd_up = pd_lb[pd_lb>=median]
        pd_down = pd_lb[pd_lb<median]
    else:
        pd_up = pd_lb[pd_lb>0]
        pd_down = pd_lb[pd_lb<=0]
    return pd_up, pd_down

def MakePros(pd_exp, list_lb, pd_survial, outfile):
    out = open(outfile+'.txt', 'w')
    out_filter = open(outfile+'.filter.txt', 'w')
    for lb in list_lb:
        pd_up, pd_down = ClassDataByMedian(pd_exp, lb)
        p_value = CalPairPvalue(pd_survial.loc[pd_up.index,:], pd_survial.loc[pd_down.index,:])
        out.write(lb+'\t'+str(p_value)+'\n')
        if p_value<0.05:
            out_filter.write(lb+'\t'+str(p_value)+'\n')
    out.close()
    out_filter.close()

def main():
    parser = argparse.ArgumentParser(description="plot Surval curve for cox result")
    parser.add_argument('-s', help='input surval file ,include OS and status columns', required=True)
    parser.add_argument('-c', help='cox result file', required=True)
    parser.add_argument('-e', help='the expression file', required=True)
    parser.add_argument('-o', help='the output file', default='LogRank')
    parser.add_argument('-p', help='the pvalue cutoff of cox analysis<<0.05>>', type=float, default=0.05)
    argv=vars(parser.parse_args())
    list_lb = HandleCoxData(argv['c'], argv['p'])
    pd_exp = HandleExpData(argv['e'])
    pd_survial = HandleExpData(argv['s'])
    MakePros(pd_exp, list_lb, pd_survial, argv['o'])


if __name__ == '__main__':
    main()
