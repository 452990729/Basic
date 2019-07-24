#!/usr/bin/env python2


import sys
import re
import argparse
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def GetData(pd_score, pd_clin):
    pd_clin = pd_clin.loc[pd_score.index,:]
    list_age = [1 if i>365*60 else 0 for i in pd_clin.loc[:, 'age_at_diagnosis']]
    list_gender = [1 if i=='male' else 0 for i in pd_clin.loc[:, 'gender']]
    list_stage = [0 if i in ['stage i', 'stage ii'] else 1 for i in pd_clin.loc[:, 'tumor_stage']]
    pd_score['Tumor stage(III+VI vs. I+II)'] = list_stage
    pd_score['Age(>= 60 vs. < 60)'] = list_age
    pd_score['Gender(male vs. female)'] = list_gender
    return pd_score

def main():
    parser = argparse.ArgumentParser(description="Get Clinical For Cox Analysis")
    parser.add_argument('-c', help='input Risk Score matrix, col are features, index are samples', required=True)
    parser.add_argument('-s', help='input survival matrix, col are features, index are samples', required=True)
    parser.add_argument('-o', help='output <<ClinicalForCox.txt>>', default='ClinicalForCox.txt')
    argv=vars(parser.parse_args())
    pd_clin = ReadData(argv['s'])
    pd_score = ReadData(argv['c'])
    pd_out = GetData(pd_score, pd_clin)
    pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
