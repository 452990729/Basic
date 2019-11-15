#!/usr/bin/env python2


import sys
import re
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def ReadAnnot(file_in):
    dict_tmp = {}
    dict_out = {}
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_split = re.split('\t', line.strip('\n'))
            for gene in re.split(';', list_split[-1]):
                if gene and gene!='NA':
                    if gene not in dict_tmp:
                        dict_tmp[gene] = [list_split[0]+':'+list_split[3],]
                    else:
                        dict_tmp[gene] += [list_split[0]+':'+list_split[3],]

    for gene in dict_tmp:
        a = 0
        b = 0
        for vls in dict_tmp[gene]:
            if float(re.split(':', vls)[1])>0:
                a += 1
            else:
                b += 1
        if a == 0 or b == 0:
            dict_out[gene] = re.split(':', dict_tmp[gene][0])[0]
    return dict_out

def MakeData(dict_in, pd_data):
    pd_out = pd.DataFrame(columns=pd_data.columns)
    list_index = []
    for gene in dict_in:
        list_index.append(gene)
        pd_out = pd_out.append(pd_data.loc[dict_in[gene],:])
    pd_out.index=list_index
    pd_out = pd_out.fillna(0)
    pd_out.to_csv('MethSwitchAnno.txt', sep='\t', header=True, index=True)

def main():
    pd_data = ReadData(sys.argv[1])
    dict_tmp = ReadAnnot(sys.argv[2])
    MakeData(dict_tmp, pd_data)


if __name__ == '__main__':
    main()
