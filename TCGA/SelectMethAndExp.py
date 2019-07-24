#!/usr/bin/env python2

import sys
import re
import argparse


def ReadMeth(file_in):
    list_up = []
    list_down = []
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_split = re.split('\t', line.strip())
            genes = list(set(re.split(';', list_split[-1])))
            if float(list_split[3])>0:
                list_up += genes
            else:
                list_down += genes
    return list_up, list_down

def ReadExp(file_in, list_up, list_down):
    hypomethylation_high = open('hypomethylation_high.txt', 'w')
    hypermethylated_lower = open('hypermethylated_lower.txt', 'w')
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_split = re.split('\t', line)
            if float(list_split[2]) > 0 and list_split[0] in list_up:
                hypermethylated_lower.write(list_split[0]+'\n')
            elif float(list_split[2]) < 0 and list_split[0] in list_down:
                hypomethylation_high.write(list_split[0]+'\n')
    hypomethylation_high.close()
    hypermethylated_lower.close()

def main():
    parser = argparse.ArgumentParser(description="define the hypomethylation_high/hypermethylated_lower of Exp and Meth")
    parser.add_argument('-exp', help='the exp diff file', required=True)
    parser.add_argument('-m', help='the meth diff file', required=True)
    argv=vars(parser.parse_args())
    list_up, list_down = ReadMeth(argv['m'])
    ReadExp(argv['exp'], list_up, list_down)


if __name__ == '__main__':
    main()
