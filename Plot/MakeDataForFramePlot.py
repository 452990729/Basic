#!/usr/bin/env python2


import sys
import re
import argparse

def MakeRef(file_in):
    dict_ref = {}
    with open(file_in, 'r') as f:
        for line in f:
            list_split = re.split('\t', line.rstrip('\n'))
            if list_split[0]:
                dict_ref[list_split[0]] = list_split[1]
    return dict_ref

def Process(file_in, dict_ref):
    index = 0
    with open(file_in, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if index == 0:
                list_sample = re.split('\t', line)[1:]
            else:
                list_split = re.split('\t', line)
                m = 0
                for vls in list_split[1:]:
                    print list_split[0]+'\t'+vls+'\t'+dict_ref[list_sample[m]]
                    m += 1
            index = 1

def main():
    parser = argparse.ArgumentParser(description="make data for frameplot")
    parser.add_argument('-i', help='input matrix, col is sample, index is feature', required=True)
    parser.add_argument('-c', help='class file', required=True)
    argv=vars(parser.parse_args())
    dict_ref = MakeRef(argv['c'])
    Process(argv['i'], dict_ref)


if __name__ == '__main__':
    main()
