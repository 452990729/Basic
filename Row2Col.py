#!/usr/bin/env python2


import re
import sys
import pandas as pd


pd_data = pd.read_csv(sys.argv[1], sep='\t', header=None)
pd_data = pd_data.T
print pd_data.to_csv(sep='\t', header=False, index=False)
