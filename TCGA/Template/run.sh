#!/bin/bash

RNACount=
RNAFPKM=
methylation=
clinical=

basepath=$(cd `dirname $0`;pwd)

########################################################
cd $basepath/0.RawData
sh run.sh $RNACount $RNAFPKM $methylation $clinical


#######################################################
cd $basepath/1.DEG
sh run.sh

########################################################
cd $basepath/2.meth
sh run.sh

########################################################
cd $basepath/3.Exp_Meth
sh run.sh

########################################################
cd $basepath/4.cox
sh run.sh

########################################################
cd $basepath/5.risk
sh run.sh

########################################################
cd $basepath/6.Clinical
sh run.sh

########################################################
cd $basepath/7.Test
sh run.sh
