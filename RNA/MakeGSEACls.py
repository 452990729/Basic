#!/usr/bin/env python2


import sys
import re
import argparse


def ReadCls(file_in):
    dict_cls = {}
    with open(file_in, 'r') as f:
        for line in f:
            list_split = re.split('\t', line.strip())
            if list_split[0]:
                dict_cls[list_split[0]] = list_split[1]
    return dict_cls

def GetData(file_in, file_out, dict_cls):
    out = open(file_out, 'w')
    with open(file_in, 'r') as f:
        list_split = re.split('\t', next(f).strip('\n'))[1:]
        out.write(' '.join([str(len(list_split)), '2', '1'])+'\n')
        out.write(' '.join(['#',]+sorted(list(set(dict_cls.values()))))+'\n')
        list_out = [dict_cls[i] for i in list_split]
        out.write(' '.join(list_out))
    out.close()

def main():
    parser = argparse.ArgumentParser(description="make gsea cls file")
    parser.add_argument('-m', help='input exp matrix', required=True)
    parser.add_argument('-c', help='input cls file', required=True)
    parser.add_argument('-o', help='output file<<gsea_cls.txt>>', default='gsea_cls.txt')
    argv=vars(parser.parse_args())
    dict_cls = ReadCls(argv['c'])
    GetData(argv['m'], argv['o'], dict_cls)


if __name__ == '__main__':
    main()
