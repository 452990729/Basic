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
                list_down += genes
            else:
                list_up += genes
    return list_up, list_down

def ReadExp(file_in, list_up, list_down):
    print 'hypomethylated: {}'.format(str(len(list_up)))
    print 'hypermethylation: {}'.format(str(len(list_down)))
    hypomethylation_high = open('hypomethylation_high.txt', 'w')
    hypermethylated_lower = open('hypermethylated_lower.txt', 'w')
    select_all = open('Exp_Meth_select.txt', 'w')
    m = 0
    n = 0
    a = 0
    b = 0
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_split = re.split('\t', line)
            if float(list_split[2]) > 0 and list_split[0] in list_up:
                hypermethylated_lower.write(list_split[0]+'\n')
                select_all.write(list_split[0]+'\n')
                m += 1
            elif float(list_split[2]) < 0 and list_split[0] in list_down:
                hypomethylation_high.write(list_split[0]+'\n')
                n += 1
                select_all.write(list_split[0]+'\n')
            if float(list_split[2]) > 0:
                a += 1
            elif float(list_split[2]) < 0:
                b += 1
    print 'Up-exp: {}'.format(str(a))
    print 'Down-exp: {}'.format(str(b))
    print 'hypermethylated_lower: {}'.format(str(m))
    print 'hypomethylation_high: {}'.format(str(n))
    hypomethylation_high.close()
    hypermethylated_lower.close()
    select_all.close()

def main():
    parser = argparse.ArgumentParser(description="define the hypomethylation_high/hypermethylated_lower of Exp and Meth")
    parser.add_argument('-exp', help='the exp diff file', required=True)
    parser.add_argument('-m', help='the meth diff file', required=True)
    argv=vars(parser.parse_args())
    list_up, list_down = ReadMeth(argv['m'])
    ReadExp(argv['exp'], list_up, list_down)


if __name__ == '__main__':
    main()
