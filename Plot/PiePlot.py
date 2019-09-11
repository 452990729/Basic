#!/usr/bin/env python2


import sys
import re
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=None, index_col=None)
    return pd_data

def MakePlot(pd_data, title, size, out):
    plt.style.use('my-paper')
    list_size = re.split(',', size)
    fig, ax = plt.subplots(figsize=(int(list_size[0]),int(list_size[1])))
    cols = list(pd_data.columns)
    x = list(np.array(pd_data.iloc[:, 0]))
    y = list(np.array(pd_data.iloc[:, 1]))
    if len(cols) == 2:
        ax.pie(y, labels=x, autopct='%1.1f%%',
                shadow=True, startangle=90)
    elif len(cols) == 3:
        explode = list(np.array(pd_data.iloc[:, 2]))
        ax.pie(y, explode=explode, labels=x, autopct='%1.1f%%',
                shadow=True, startangle=90)
    ax.axis('equal')
    ax.set_title(title)
    plt.savefig('{}.pdf'.format(out), dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make pieplot")
    parser.add_argument('-m', help='input matrix, col0 is label, col1 is size col2 is explode(whether), no header and index', required=True)
    parser.add_argument('-title', help='th title of pieplot', default='')
    parser.add_argument('-size', help='the figsize of pieplot, width,height, <<10,15>>', default='10,15')
    parser.add_argument('-out', help='the output of pieplot', default='Pieplot')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    MakePlot(pd_data, argv['title'], argv['size'], argv['out'])


if __name__ == '__main__':
    main()
