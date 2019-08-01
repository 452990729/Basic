#!usr/bin/env python2


import sys
import re
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def TPM2FPKM(pd_data):
    pd_sum = pd_data.sum(axis=1)

