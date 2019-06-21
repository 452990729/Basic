#!/usr/bin/env python2


import sys
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegressionCV, LassoCV
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

BasePath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(BasePath+'/Module')
from CrossValidator import RunValidator

def GetData(file_in):
    pd_data =pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def RunLasso(feature, response):
    clf = LassoCV(alphas = [1, 0.1, 0.001, 0.0005]).fit(feature, response)
    coef = pd.Series(clf.coef_, index = feature.columns)
    coef.to_csv('Lasso.coef.txt', sep='\t', index=True, header=False)

def RunSVM(feature, response):
    SVM = svm.SVC(C=0.5, probability=True, class_weight='balanced')
    RunValidator('bina', feature, response, SVM, 5)

def RunRF(feature, response, testf=None, testr=None):
    RandomForest = RandomForestClassifier(n_estimators=50, max_depth=10, oob_score=True, class_weight='balanced')
    RunValidator('bina', feature, response, RandomForest, 5)

def RunLogistic(feature, response, testf=None, testr=None):
    Logistic = LogisticRegressionCV(multi_class="ovr",fit_intercept=True,\
                               Cs=np.logspace(-2,2,20),cv=2,penalty="l2",\
                               solver="lbfgs",tol=0.01,class_weight='balanced')
    RunValidator('bina', feature, response, Logistic, 5)

def main():
    feature_date = GetData(sys.argv[2])
    response_date = GetData(sys.argv[3])
    if sys.argv[1] == 'Lasso':
        RunLasso(feature_date, response_date)
    elif sys.argv[1] == 'SelectModel':
        RunSVM(feature_date, response_date)
        RunRF(feature_date, response_date)
        RunLogistic(feature_date, response_date)
    elif sys.argv[1] == 'SVM':
        RunSVM(feature_date, response_date)
    elif sys.argv[1] == 'RandomForest':
        RunRF(feature_date, response_date)
    elif sys.argv[1] == 'Logistic':
        RunLogistic(feature_date, response_date)
    else:
        print 'WRONG CHOICE!'


if __name__ == '__main__':
    main()

