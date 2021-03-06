#!/usr/bin/env python2

import re
import random
import argparse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0, dtype='a')
    return pd_data

def ReadClass(file_in):
    dict_tmp = {}
    with open(file_in, 'r') as f:
        for line in f:
            list_split = re.split('\t', line.rstrip())
            if list_split[0]:
                if list_split[1] not in dict_tmp:
                    dict_tmp[list_split[1]] = [list_split[0],]
                else:
                    dict_tmp[list_split[1]] += [list_split[0],]
    return dict_tmp

def MakePCA(pd_data, num=2):
    pd_data = pd_data.T
    pca=PCA(n_components=num)
    reduced_data=pca.fit_transform(pd_data)
    return pd.DataFrame(reduced_data, index=pd_data.index),\
            [round(i*100, 2) for i in pca.explained_variance_ratio_]

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    cap = plt.cm.get_cmap(name, n+1)
    list_tmp = [cap(i) for i in range(n)]
    random.shuffle(list_tmp)
    return list_tmp

def MakePlot(pd_data, dict_class, pca_variance, out_prefix, anno=False):
    keys = sorted(dict_class.keys())
    list_color = get_cmap(len(keys))
    plt.style.use('my-paper')
    fig, ax = plt.subplots(figsize=(16,16))
    m = 0
    for key in keys:
        pd_sub = pd_data.loc[dict_class[key], :]
        x = pd_sub.iloc[:, 0]
        y = pd_sub.iloc[:, 1]
        ax.scatter(x, y, c=[list_color[m], ],  marker='o',\
                    alpha=0.5, edgecolors='none', label=key)
        m += 1
        if anno:
            for i, txt in enumerate(pd_sub.index):
                ax.annotate(txt, (x[i], y[i]), fontsize=8)
#        else:
#    ax.set_xlim([-25000, 30000])
#    ax.set_ylim([-5000, 20000])
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    ax.set_xlabel('PC1: {}%'.format(pca_variance[0]))
    ax.set_ylabel('PC2: {}%'.format(pca_variance[1]))
    pd_data.to_csv('{}_variance.txt'.format(out_prefix), sep='\t', header=True, index=True)
    plt.savefig('{}_pca.pdf'.format(out_prefix))


def main():
    parser = argparse.ArgumentParser(description="2D PCA analysis")
    parser.add_argument('-m', help='input feature matrix, features in rows, samples in columns', required=True)
    parser.add_argument('-c', help='class file')
    parser.add_argument('-anno', help='annotate sample or not', action='store_true')
    parser.add_argument('-o', help='output prefix<<out>>', default='out')
    argv=vars(parser.parse_args())
    pd_raw = ReadData(argv['m'])
    pd_data, pca_variance = MakePCA(pd_raw)
    if argv['c']:
        dict_class = ReadClass(argv['c'])
    else:
        dict_class = {'Sample':list(pd_data.index)}
    MakePlot(pd_data, dict_class, pca_variance, argv['o'], argv['anno'])


if __name__ == '__main__':
    main()
