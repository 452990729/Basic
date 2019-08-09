#!/usr/bin/env python2

import argparse
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def MakePlot(pd_data):
    data_x = range(pd_data.shape[0])
    data_hight = list(np.array(pd_data.iloc[:,0].T))
    data_color = list(np.array(pd_data.iloc[:,1].T))
    data_color = [x / max(data_color) for x in data_color]
    plt.style.use(['my-paper'])
    fig, axe = plt.subplots(figsize=(10, 12))
    my_cmap = plt.cm.get_cmap('bwr')
    colors = my_cmap(data_color)
    rects = axe.barh(data_x, data_hight, color=colors)
    sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0,max(data_color)))
    sm.set_array([])
#    CS = plt.contourf([data_x, data_color],cmap=my_cmap)
    cbar = plt.colorbar(sm)
    cbar.set_label('Color', rotation=270,labelpad=25)
    axe.set_yticklabels(pd_data.index)
    plt.savefig('HeatBar.pdf', dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make HeatBar plot")
    parser.add_argument('-m', help='input matrix, index is gene, col1 is value, col2 is color', required=True)
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    MakePlot(pd_data)


if __name__ == '__main__':
    main()
