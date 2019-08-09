#!/usr/bin/env python2


import argparse
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def MakePlot(pd_data):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    shapes = [".", ""]
    plt.style.use(['my-paper', 'my-line'])
    fig,axe = plt.subplots(figsize=(30,10))
    ct = 1
    for index in pd_data.index:
        axe.plot((pd_data.loc[index,'lower 0.95'], pd_data.loc[index,'upper 0.95']),
                (ct, ct), colors[ct-1], lw=8)
        axe.plot((pd_data.loc[index,'lower 0.95'], pd_data.loc[index,'lower 0.95']),
                 (ct-0.1, ct+0.1), colors[ct-1], lw=6)
        axe.plot((pd_data.loc[index,'upper 0.95'], pd_data.loc[index,'upper 0.95']),
                 (ct-0.1, ct+0.1), colors[ct-1], lw=6)
#        print pd_data.loc[index,'coef']
        axe.scatter([pd_data.loc[index,'coef']],[ct], marker='D', s=500, alpha=1)
        ct += 1
    axe.set_xlabel('log(HR) (95% CI)', size=30)
    plt.yticks(size = 20)
    axe.set_yticks(range(1,ct))
    axe.set_yticklabels(pd_data.index, size=20)
    axe.set_ylim(0.5, (ct-1)*1.2)
    axe.set_xlim(pd_data.loc[:,'lower 0.95'].min()*1.2, pd_data.loc[:,'upper 0.95'].max()*1.2)
#    plt.setp(axe.spines.values(), linewidth=8)
    plt.savefig('Forest.pdf', dpi=300)

def main():
    parser = argparse.ArgumentParser(description="make Forest plot")
    parser.add_argument('-m', help='input matrix, cox result', required=True)
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['m'])
    MakePlot(pd_data)


if __name__ == '__main__':
    main()
