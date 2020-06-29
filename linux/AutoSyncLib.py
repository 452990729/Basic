#!/usr/bin/env python

import os
import subprocess


def GetLib(node, path):
    a = subprocess.Popen(['/mnt/dfc_data1/software/anaconda2/bin/pssh', '-i', '-H', node, '/GetFile.py',\
                          path], stdout=subprocess.PIPE)
    out = [i.strip('\n') for i in  a.stdout.readlines()[1:]]
    return out

def GetLocal(path):
    root, dirs, files = next(os.walk(path))
    list_tmp = []
    for dr in dirs:
        list_tmp.append(dr)
    for fl in files:
        list_tmp.append(fl)
    return list_tmp

def Diff(list1, list2, node, path):
    set1 = set(list2)
    for f in list1:
        if f not in set1:
            os.system('scp {} {}'.format(os.path.join(path, f),\
                                         node+':'+os.path.join(path, f)))

def main():
#    Lib = GetLocal('/lib')
    Lib64 = GetLocal('/lib64')
#    UsrLib = GetLocal('/usr/lib')
    UsrLib64 = GetLocal('/usr/lib64')
#    UsrBin = GetLocal('/usr/bin')
    list_node = ['compute-0-1', 'compute-0-2', 'compute-0-3', 'compute-0-4', 'compute-0-5', 'compute-0-6', 'compute-0-7']
    for node in list_node:
#        list_lib = GetLib(node, '/lib')
        list_lib64 = GetLib(node, '/lib64')
#        list_usrlib = GetLib(node, '/usr/lib')
        list_usrlib64 = GetLib(node, '/usr/lib64')
#        list_usrbin =  GetLib(node, '/usr/bin')
#        Diff(Lib, list_lib, node, '/lib')
        Diff(Lib64, list_lib64, node, '/lib64')
#        Diff(UsrLib, list_usrlib, node, '/usr/lib')
        Diff(UsrLib64, list_usrlib64, node, '/usr/lib64')
#        Diff(UsrBin, list_usrbin, node, '/usr/bin')


if __name__ == '__main__':
    main()
