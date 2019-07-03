#!/usr/bin/env python2

import sys
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def MakePCA(pd_data, num=2):
    pca=PCA(n_components=num)
    reduced_data=pca.fit_transform(pd_data)
    return reduced_data

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    cap = plt.cm.get_cmap(name, n+1)
    list_tmp = [cap(i) for i in range(n)]
    random.shuffle(list_tmp)
    return list_tmp

def 
