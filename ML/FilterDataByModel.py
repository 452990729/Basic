#!/usr/bin/env python2


import sys
import numpy as np
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


def GetData(file_in):
    pd_data =pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def SelectFeature(X, Y, model, num):
    if model == 'Logistic':
        estimator  = LogisticRegression(class_weight='balanced')
    elif model == 'SVM':
        estimator = SVC(class_weight='balanced')
    selector = RFE(estimator=estimator, n_features_to_select=num).fit(X, np.array(Y.T)[0])
    X_filter = X[X.columns[selector.get_support(indices=True)]]
    X_filter.to_csv('FeatureFilterByModle.txt', sep='\t', header=True, index=True)

def main():
    X = GetData(sys.argv[1])
    Y = GetData(sys.argv[2])
    SelectFeature(X, Y, 'Logistic', int(sys.argv[3]))


if __name__ == '__main__':
    main()

