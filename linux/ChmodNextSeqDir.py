#!/usr/bin/env python3


import sys
import os
from glob import glob

def CheckRootDir(path_in):
    list_dr = []
    root, drs, files = next(os.walk(path_in))
    for dr in drs:
        dr_path = os.path.join(root, dr)
        if os.access(dr_path, os.W_OK):
            if glob(dr_path+'/CopyComplete.txt'):
                list_dr.append(dr_path)
    return list_dr

def ChmodDir(path_in):
    os.system('chmod 555 {}'.format(path_in))
    root, drs, files = next(os.walk(path_in))
    for fl in files:
        os.system('chmod 444 {}'.format(os.path.join(root, fl)))
    for dr in drs:
         ChmodDir(os.path.join(root, dr))

def main():
    list_path = CheckRootDir(sys.argv[1])
    for path_in in list_path:
        print('BEG chmod {}'.format(path_in))
        ChmodDir(path_in)
        print('END chmod {}'.format(path_in))
if __name__ == '__main__':
    main()
