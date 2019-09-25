#!/usr/bin/env python2


import re
import os
import argparse
import json
import pandas as pd

BasePath = os.path.split(os.path.realpath(__file__))[0]

def ReadRef(file_in):
    with open(file_in, 'r') as f:
        return json.load(f)

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def SwitchID(dict_go, dict_gonamespace, pd_data):
    label = []
    namespace = []
    for index in pd_data.index:
        if index in dict_go:
            label.append(dict_go[index])
            namespace.append(dict_gonamespace[index])
        else:
            label.append(index)
            namespace.append(index)
    pd_data.index = label
    pd_data.insert(0, 'namespace', namespace)
    return pd_data

def main():
    parser = argparse.ArgumentParser(description="Switch go index")
    parser.add_argument('-m', help='input matrix, index are go', required=True)
    parser.add_argument('-o', help='output file<<GOAnnotation.txt>>', required='GOAnnotation.txt')
    argv=vars(parser.parse_args())
    dict_go = ReadRef(BasePath+'/../../Database/GO/go.json')
    dict_gonamespace = ReadRef(BasePath+'/../../Database/GO/gonamespace.json')
    pd_data = ReadData(argv['m'])
    pd_out = SwitchID(dict_go, dict_gonamespace, pd_data)
    pd_out.to_csv(argv['o'], sep='\t', header=True, index=True)


if __name__ == '__main__':
    main()
