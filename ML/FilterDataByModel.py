#!/usr/bin/env python2


import sys
import argparse
import numpy as np
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression,LassoCV
from sklearn.svm import SVC


def GetData(file_in):
    pd_data =pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def RunLasso(feature, response):
    clf = LassoCV(alphas = [1, 0.1, 0.001, 0.0005]).fit(feature, response)
    coef = pd.Series(clf.coef_, index = feature.columns)
    coef.to_csv('Lasso.coef.txt', sep='\t', index=True, header=False)

def SelectFeature(X, Y, model, num):
    if model == 'Logistic':
        estimator  = LogisticRegression(class_weight='balanced')
        selector = RFE(estimator=estimator, n_features_to_select=num).fit(X, np.array(Y.T)[0])
        X_filter = X[X.columns[selector.get_support(indices=True)]]
        X_filter.to_csv('FeatureFilterByModle.txt', sep='\t', header=True, index=True)
    elif model == 'SVM':
        estimator = SVC(class_weight='balanced')
        selector = RFE(estimator=estimator, n_features_to_select=num).fit(X, np.array(Y.T)[0])
        X_filter = X[X.columns[selector.get_support(indices=True)]]
        X_filter.to_csv('FeatureFilterByModle.txt', sep='\t', header=True, index=True)
    elif model == 'Lasso':
        RunLasso(X, Y)
#    X_filter.to_csv('FeatureFilterByModle.txt', sep='\t', header=True, index=True)

def main():
    parser = argparse.ArgumentParser(description="Mathine learning model used to filter feature")
    parser.add_argument('-x', help='input feature matrix, col are features, index are samples', required=True)
    parser.add_argument('-y', help='input response matrix, col is response, index are samples', required=True)
    parser.add_argument('-m', help='the method used <<Logistic>>', choices=['SVM', 'Lasso', 'Logistic'], default='Logistic')
    parser.add_argument('-n', help='if use svm/Logistic, the number of features to keep<<20>>', type=int, default=20)
    argv=vars(parser.parse_args())
    X = GetData(argv['x'])
    Y = GetData(argv['y'])
    SelectFeature(X, Y, argv['m'], argv['n'])


if __name__ == '__main__':
    main()

