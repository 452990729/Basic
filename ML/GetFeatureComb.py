#!/usr/bin/env python2


import re
import sys
import argparse
import random
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegressionCV
from sklearn.svm import SVC,LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, accuracy_score, f1_score, recall_score, precision_score

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def SplitData(X, Y, frac):
    x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size = frac)
    return x_train,x_test,y_train,y_test

def GetModle(tp):
    if tp == 'SVM':
        return SVC(C=0.5, probability=True, class_weight='balanced', kernel='linear')
    elif tp == 'LR':
        return LogisticRegressionCV(fit_intercept=True,Cs=np.logspace(-2,2,20),cv=2,penalty="l2",solver="lbfgs",tol=0.01,class_weight='balanced')

def Predict(feature, response, model):
    y_score = model.predict_proba(feature)[:,1]
    y_test = response
    y_pred = model.predict(feature)
    fpr, tpr, _ = roc_curve(y_test, y_score)
    accuracy_value = accuracy_score(y_test, y_pred)
    precision_value = precision_score(y_test, y_pred)
    recall_value = recall_score(y_test, y_pred)
    f1_value = f1_score(y_test, y_pred)
    auc_value = auc(fpr, tpr)
    return accuracy_value,precision_value,recall_value,f1_value,auc_value,fpr,tpr

def get_cmap(n, name='hsv'):
    cap = plt.cm.get_cmap(name, n+1)
    list_tmp = [cap(i) for i in range(n)]
    random.shuffle(list_tmp)
    return list_tmp

def PlotROC(ax, color, fpr, tpr):
    ax.plot(fpr, tpr, 'k-', lw=2, color=color)
    return ax

def Strip(X, Y, tp, bootstrap):
    list_b = ['B'+str(i) for i in range(1,bootstrap+1)]
    pd_feature = pd.DataFrame(index=list_b, columns=X.columns)
    out = open('Ml.stat', 'w')
    out.write(' \tauc\taccuracy\tprecision\trecall\tF1')
    plt.style.use(['my-paper', 'my-line'])
    colors = ['darkorange', 'blue', 'red', 'yellow']
    fig, ax = plt.subplots(figsize=(10,8))
    ax.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6))
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlabel('1-Specificity')
    ax.set_ylabel('Sensitivity')
    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_visible(True)
    colors = get_cmap(bootstrap, 'summer')
    m = 0
    auc_all = 0
    for i in list_b:
        x_train,x_test,y_train,y_test = SplitData(X, Y, 0.2)
        model = GetModle(tp)
        mbs = model.fit(x_train,y_train)
        pd_feature.loc[i,:] = mbs.coef_
        accuracy_value,precision_value,recall_value,f1_value,auc_value,fpr,tpr = Predict(x_test,y_test,mbs)
        out.write(i+'\t'+str(auc_value)+'\t'+str(accuracy_value)+'\t'+str(precision_value)+'\t'+str(recall_value)+'\t'+str(f1_value)+'\n')
        PlotROC(ax, colors[m], fpr, tpr)
        m += 1
        auc_all += auc_value
    ax.set_title('Mean AUC: {}'.format(round(auc_all/200, 2)), size=30)
    pd_feature.to_csv('feature_weight.txt', sep='\t', header=True, index=True)
    fig.savefig('All_ROC.pdf')

def main():
    parser = argparse.ArgumentParser(description="Mathine learning feature evaluation")
    parser.add_argument('-x', help='input feature matrix, col are features, index are samples', required=True)
    parser.add_argument('-y', help='input response matrix, col is response, index are samples', required=True)
    parser.add_argument('-m', help='if use predict mode, the method used <<svm>>', choices=['svm', 'LR',], default='svm')
    parser.add_argument('-b', help='if use validator mode, bootstrap time <<200>>', type=int, default=200)
    argv=vars(parser.parse_args())
    X = ReadData(argv['x'])
    Y = ReadData(argv['y'])
    tp = argv['m']
    Strip(X, Y, tp, int(argv['b']))


if __name__ == '__main__':
    main()
