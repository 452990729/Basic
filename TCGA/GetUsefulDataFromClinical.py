#!/usr/bin/env python2


import os
import re
import argparse
import pandas as pd

def ReadData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def GetOS(pd_data):
    pd_os = pd.DataFrame(index=pd_data.index, columns=['OS'])
    pd_status = pd.DataFrame(index=pd_data.index, columns=['status'])
    total = pd_data.shape[0]
    for i in range(total):
        days_to_last_follow_up = pd_data['days_to_last_follow_up'].iloc[i]
        days_to_death = pd_data['days_to_death'].iloc[i]
        status = pd_data['vital_status'].iloc[i]
        if days_to_last_follow_up != 'NA':
            pd_os.iloc[i] = days_to_last_follow_up
        else:
            pd_os.iloc[i] = days_to_death
        if status == 'Alive':
            pd_status.iloc[i] = 0
        elif status == 'Dead':
            pd_status.iloc[i] = 1
        else:
            pd_status.iloc[i] = 'NA'
    return pd_os, pd_status

def MakeData(pd_data, pd_os, pd_status, outfile):
    list_useful = ['year_of_diagnosis', 'primary_diagnosis',\
                  'tumor_stage', 'tissue_or_organ_of_origin',\
                  'days_to_last_follow_up', 'weight', 'bmi',\
                  'height', 'gender', 'year_of_birth', 'race',\
                  'vital_status', 'age_at_index', 'days_to_death',\
                  'treatments_pharmaceutical_treatment_type',\
                  'bcr_patient_barcode', 'disease']
    pd_out = pd_data.loc[:, list_useful]
    pd_out['OS'] = pd_os
    pd_out['status'] = pd_status
    pd_out.index=pd_data['submitter_id']
    pd_out.to_csv(outfile, sep='\t', index=True, header=True)

def main():
    parser = argparse.ArgumentParser(description="Extract Useful Data From TCGA Clinical File")
    parser.add_argument('-i', help='input TCGA Clinical File', required=True)
    parser.add_argument('-o', help='output file <<ClinicalUseful.txt>>', default='ClinicalUseful.txt')
    argv=vars(parser.parse_args())
    pd_data = ReadData(argv['i'])
    pd_os, pd_status = GetOS(pd_data)
    MakeData(pd_data, pd_os, pd_status, argv['o'])


if __name__ == '__main__':
    main()
