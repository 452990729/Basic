#!/usr/bin/env python2


import sys
import re
import os
import argparse
import pandas as pd


BasePath = os.path.split(os.path.realpath(__file__))[0]
SurvialCurve = BasePath+'/SurvialCurve.py'

def HandleCoxData(file_in, p):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    pd_filter = pd_data[pd_data['p']<=p]
    return list(pd_filter.index)

def HandleExpData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ClassDataByMedian(pd_exp, label):
    pd_lb = pd_exp.loc[:, label]
    median = pd_lb.median()
    if median != 0:
        pd_up = pd_lb[pd_lb>=median]
        pd_down = pd_lb[pd_lb<median]
    else:
        pd_up = pd_lb[pd_lb>0]
        pd_down = pd_lb[pd_lb<=0]
    pd_up[:] = 'high expression'
    pd_down[:] = 'low expression'
    pd_all = pd_up.append(pd_down)
    pd_all.to_csv('{}_cluster.txt'.format(label), sep='\t', header=True, index=True)

def MakePros(pd_exp, list_lb, file_surval, trim):
    for lb in list_lb:
        ClassDataByMedian(pd_exp, lb)
        os.system('{} -s {} -c {}_cluster.txt -t {} -trim {}'.format(SurvialCurve, file_surval, lb, lb, trim))

def main():
    parser = argparse.ArgumentParser(description="plot Surval curve for cox result")
    parser.add_argument('-s', help='input surval file ,include OS and status columns', required=True)
    parser.add_argument('-c', help='cox result file', required=True)
    parser.add_argument('-e', help='the expression file', required=True)
    parser.add_argument('-p', help='the pvalue cutoff of cox analysis<<0.05>>', type=float, default=0.05)
    parser.add_argument('-t', help='survival time trim <<1825>>', default=1825)
    argv=vars(parser.parse_args())
    list_lb = HandleCoxData(argv['c'], argv['p'])
    pd_exp = HandleExpData(argv['e'])
    MakePros(pd_exp, list_lb, argv['s'], argv['t'])


if __name__ == '__main__':
    main()
