#!/usr/bin/env python

import os
import sys
import subprocess
import re
import argparse

def rm_data(path_in, ex):
    tuple_path = next(os.walk(path_in))
    list_dir = [os.path.join(tuple_path[0], dir) for dir in tuple_path[1]]
    list_file = [os.path.join(tuple_path[0], file) for file in tuple_path[2]]
    for file_s in list_file:
        if file_s.endswith('.sam') or file_s.endswith('.bam'):
            if ex == 'remove':
                child = subprocess.Popen(['rm', file_s])
                child.wait()
            elif ex == 'print':
                print file_s
        else:
            pass
    for dir in list_dir:
        rm_data(dir, ex)

def main():
    parser = argparse.ArgumentParser(description="remove bam/sam files")
    parser.add_argument('-i', help='input path', required=True)
    parser.add_argument('-t', help='remove or print<<>print>', choices=['remove', 'print'], default='print')
    argv=vars(parser.parse_args())
    rm_data(argv['i'], argv['t'])

if __name__ == '__main__':
    main()
