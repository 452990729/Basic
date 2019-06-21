#!/usr/bin/env python2

import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier

BasePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(BasePath+'/Module')
import CrossValidator


def HandleData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    pd_feature = pd_data.iloc[:, :-1]
    pd_class = pd_data.iloc[:, -1]
    return pd_feature, pd_class

def RandomRF(pd_feature, pd_class):
    forest = RandomForestClassifier(n_estimators=100, random_state=1, max_depth=10, oob_score=True, class_weight='balanced')
    One_Rest_Classifier = OneVsRestClassifier(forest)
    CrossValidator.RunValidator('multi', pd_feature, pd_class, One_Rest_Classifier, 5)

def main():
    pd_feature, pd_class = HandleData(sys.argv[1])
    RandomRF(pd_feature, pd_class)

if __name__ == '__main__':
    main()

