#!/bin/bash

mkdir RawData
~/Software/anaconda2/envs/aspera-3.7.7/bin/ascp -QT -l 400m -P 33001 -k 1 -i ~/Software/anaconda2/envs/aspera-3.7.7/etc/asperaweb_id_dsa.openssh --mode recv --host fasp.sra.ebi.ac.uk --user era-fasp --file-list=$1 RawData
