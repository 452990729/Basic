#!/bin/bash

RNACount=
RNAFPKM=
methylation=
clinical=

########################################################
cd 0.RawData
sh run.sh $RNACount $RNAFPKM $methylation $clinical


#######################################################
cd 1.DEG
sh run.sh

########################################################
cd 2.meth
sh run.sh

########################################################
cd 3.Exp_Meth
sh run.sh

########################################################
cd 4.cox
sh run.sh

########################################################
cd 5.risk
sh run.sh

########################################################
cd 6.Clinical
sh run.sh

########################################################
cd 7.Test
sh run.sh
