#!/usr/bin/env python2


import sys
import re
import os
import argparse
import pandas as pd


BasePath = os.path.split(os.path.realpath(__file__))[0]
SurvialCurve = BasePath+'/SurvialCurve.py'

def HandleExpData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ClassDataByMedian(pd_exp, lb):
    pd_lb = pd_exp.loc[:, 'RiskScore']
    median = pd_lb.median()
    pd_up = pd_lb[pd_lb>=median]
    pd_up[:] = 'High {}'.format(lb)
    pd_down = pd_lb[pd_lb<median]
    pd_down[:] = 'Low {}'.format(lb)
    pd_all = pd_up.append(pd_down)
    pd_all.to_csv('HighLow_cluster.txt', sep='\t', header=True, index=True)

def MakePros(pd_exp, file_surval, trim, lb):
    ClassDataByMedian(pd_exp, lb)
    os.system('{} -s {} -c HighLow_cluster.txt -trim {}'.format(SurvialCurve, file_surval, trim))

def main():
    parser = argparse.ArgumentParser(description="plot Surval curve for high-low feature")
    parser.add_argument('-s', help='input surval file ,include OS and status columns', required=True)
    parser.add_argument('-e', help='the feature value file', required=True)
    parser.add_argument('-t', help='survival time trim <<1825>>', default=1825)
    parser.add_argument('-l', help='survival label <<expression>>', default='expression')
    argv=vars(parser.parse_args())
    pd_exp = HandleExpData(argv['e'])
    MakePros(pd_exp, argv['s'], argv['t'], argv['l'])


if __name__ == '__main__':
    main()
