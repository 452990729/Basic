#!/bin/bash

RNACount=$1
RNAFPKM=$2
methylation=$3
clinical=$4

/home/lixuefei/Pipeline/Basic/TCGA/GetUsefulDataFromClinical.py -i $clinical
/home/lixuefei/Pipeline/Basic/TCGA/GetTCGAClinicalStatusFromTime.py -s ClinicalUseful.txt
/home/lixuefei/Pipeline/Basic/TCGA/GetSampleOvaelap.py -s ClinicalUseful.txt -rc $RNACount -rf $RNAFPKM -m $methylation
/home/lixuefei/Pipeline/Basic/GeneIDTk.py switch -m TCGA-RNACount.txt
mv SwitchMatrix.txt TCGA-RNACountSwitch.txt
/home/lixuefei/Pipeline/Basic/GeneIDTk.py switch -m TCGA-RNAFPKM.txt
mv SwitchMatrix.txt TCGA-RNAFPKMSwitch.txt
mkdir Final
/home/lixuefei/Pipeline/Basic/TCGA/SplitTCGAType.py -rc TCGA-RNACountSwitch.txt -rf TCGA-RNAFPKMSwitch.txt -m TCGA-METH.txt -o Final
cd ../
