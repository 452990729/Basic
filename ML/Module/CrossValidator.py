#!/usr/bin/env python2


import re
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import interp, stats
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve, auc
from compare_auc_delong import delong_roc_variance


def PlotROC(ax, lb, color, fpr, tpr, auc, ci):
    ax.plot(fpr, tpr, 'k-', lw=2, label='{}AUC(%95 CI) = {}({}))'.\
           format(lb, str(round(auc, 2)), '-'.join([str(round(i, 2)) for i in ci])), color=color)
    return ax

def MultiClass(feature, response, model, fold):
    skf = StratifiedKFold(n_splits=fold, random_state=None, shuffle=False)
    response_befor = response
    response = pd.DataFrame(label_binarize(response, classes=list(set(list(response)))))
    n_classes = response.shape[1]
    micro_mean_tpr = 0.0
    micro_mean_fpr = np.linspace(0, 1, 100)
    macro_mean_tpr = 0.0
    macro_mean_fpr = np.linspace(0, 1, 100)
    for train_index, test_index in skf.split(feature, response_befor):
        fpr = {}
        tpr = {}
        mbs = model.fit(feature.iloc[train_index], np.array(response.iloc[train_index]),)
        y_score = mbs.predict_proba(feature.iloc[test_index])[:,1]
        y_test = np.array(response.iloc[test_index])
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        fpr["micro"], tpr["micro"], _  = roc_curve(y_test.ravel(), y_score.ravel())
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += interp(all_fpr, fpr[i], tpr[i])
        mean_tpr /= n_classes
        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        micro_mean_tpr += interp(micro_mean_fpr, fpr["micro"], tpr["micro"])
        macro_mean_tpr += interp(micro_mean_fpr, fpr["macro"], tpr["macro"])
        micro_mean_tpr[0] = 0.0
        macro_mean_tpr[0] = 0.0
    micro_mean_tpr /= fold
    macro_mean_tpr /= fold
    micro_mean_tpr[-1] = 1.0
    macro_mean_tpr[-1] = 1.0
    micro_auc = auc(micro_mean_fpr, micro_mean_tpr)
    macro_auc = auc(macro_mean_fpr, macro_mean_tpr)
    return micro_mean_fpr, micro_mean_tpr, micro_auc,\
            macro_mean_fpr, macro_mean_tpr, macro_auc

def BinaClass(feature, response, model, fold):
    skf = StratifiedKFold(n_splits=fold, random_state=None, shuffle=False)
    list_y_score = []
    list_y_test = []
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    for train_index, test_index in skf.split(feature, response):
        mbs = model.fit(feature.iloc[train_index], response.iloc[train_index],)
        y_score = mbs.predict_proba(feature.iloc[test_index])[:,1]
        y_test = response.iloc[test_index]
        list_y_score += list(y_score)
        list_y_test += list(np.array(y_test.T))
        fpr, tpr, _ = roc_curve(y_test, y_score)
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
    mean_tpr /= fold
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    auc_value, ci = GetAUC(np.array(list_y_test), np.array(list_y_score))
    return mean_fpr, mean_tpr, auc_value, ci

def GetAUC(np_test, np_predict):
    alpha=0.95
    auc_value, auc_cov = delong_roc_variance(np_test, np_predict)
    auc_std = np.sqrt(auc_cov)
    lower_upper_q = np.abs(np.array([0, 1]) - (1 - alpha) / 2)
    ci = stats.norm.ppf(lower_upper_q, loc=auc_value, scale=auc_std)
    return auc_value,ci

def Predict(feature, response, model):
    y_score = model.predict_proba(feature)[:,1]
    y_test = response
    fpr, tpr, _ = roc_curve(y_test, y_score)
    auc_value, ci = GetAUC(np.array(list(np.array(y_test.T))), np.array(list(y_score)))
    return fpr, tpr, auc_value, ci

def MakeROC(tp, feature, response, model, test_x=None, test_y=None, fold=5):
    plt.style.use(['my-paper', 'my-line'])
    fig, ax = plt.subplots(figsize=(10,8))
    ax.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6))
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlabel('1-Specificity')
    ax.set_ylabel('Sensitivity')
    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_visible(True)
    if tp in ['multi', 'bina']:
        for col in response.columns:
            RunValidator(tp, feature, response.loc[:,col], model, fold, ax, col)
    elif tp == 'predict':
        m = 0
        for col in response.columns:
            mbs = model.fit(feature, response.iloc[:,m],)
            fpr, tpr, auc_value, ci = Predict(test_x, test_y.loc[:, col], mbs)
            PlotROC(ax, col, 'darkorange', fpr, tpr, auc_value, ci)
            m += 1
    ax.legend(loc="lower right")
    plt.savefig('{}_ROC.pdf'.format(re.split('\(', str(model))[0]))

def RunValidator(tp, feature, response, model, fold, ax, lb):
    if tp == 'multi':
        micro_mean_fpr, micro_mean_tpr, micro_auc, macro_mean_fpr, macro_mean_tpr, macro_auc =\
                MultiClass(feature, response, model, fold=fold)
        PlotROC(ax, 'micro-average ', 'deeppink', micro_mean_fpr, micro_mean_tpr, micro_auc)
        PlotROC(ax, 'macro-average ', 'navy', macro_mean_fpr, macro_mean_tpr, macro_auc)
    elif tp == 'bina':
        mean_fpr, mean_tpr, mean_auc, ci = BinaClass(feature, response, model, fold)
        PlotROC(ax, lb, 'darkorange', mean_fpr, mean_tpr, mean_auc, ci)

