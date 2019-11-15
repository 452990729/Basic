#!/bin/bash

/home/lixuefei/Pipeline/Basic/ExtractById.py -m ../3.Exp_Meth/Exp_Meth_select_FPKM_Cancer.txt -i ../0.RawData/Final/TrainCancerClass.txt -col
/home/lixuefei/Pipeline/Basic/TCGA/TrimTCGALongID.py -i ExtractData.txt
/home/lixuefei/Pipeline/Basic/Row2Col.py TrimedMatrix.txt > GeneSelect.txt
rm ExtractData.txt TrimedMatrix.txt
mkdir univariate
cd univariate
/home/lixuefei/Pipeline/Basic/Survial/CoxSurvial.py -t univariate -s ../../0.RawData/ClinicalUseful.txt -c ../GeneSelect.txt
awk -F"\t" '{if($6<0.05) print $0}' CoxRegress.txt > CoxRegressDiff005.txt
/home/lixuefei/Pipeline/Basic/ExtractById.py -m ../GeneSelect.txt -i CoxRegressDiff005.txt -o CoxRegressDiff005FPKM.txt -col

cd ..
mkdir multivariable
cd multivariable
/home/lixuefei/Pipeline/Basic/Survial/CoxSurvial.py -t multivariable -s ../../0.RawData/ClinicalUseful.txt -c ../univariate/CoxRegressDiff005FPKM.txt
awk -F"\t" '{if($6<0.05) print $0}' CoxRegress.txt > CoxRegressDiff005.txt
/home/lixuefei/Pipeline/Basic/Survial/CoxGeneSurvial.py -s ../../0.RawData/ClinicalUseful.txt -c CoxRegress.txt -e ../univariate/CoxRegressDiff005FPKM.txt
/home/lixuefei/Pipeline/Basic/ExtractById.py -m CoxRegress.txt -i LogRank.filter.txt -o CoxRegressDiff005LogRankCoef.txt
/home/lixuefei/Pipeline/Basic/ExtractById.py -m ../GeneSelect.txt -i LogRank.filter.txt -o CoxRegressDiff005LogRankFPKM.txt -col
/home/lixuefei/Pipeline/Basic/ExtractById.py -m CoxRegress.txt -i CoxRegressDiff005.txt -o CoxRegressDiff005Coef.txt
/home/lixuefei/Pipeline/Basic/ExtractById.py -m ../GeneSelect.txt -i CoxRegressDiff005.txt -o CoxRegressDiff005FPKM.txt -col
mkdir Survival
cd Survival
/home/lixuefei/Pipeline/Basic/Survial/CoxGenePlotSurvial.py -s ../../../0.RawData/ClinicalUseful.txt -c ../CoxRegressDiff005Coef.txt -e ../CoxRegressDiff005FPKM.txt
cd ../
/home/lixuefei/Pipeline/Basic/TCGA/GetGeneForBoxplot.py -e ../../3.Exp_Meth/Exp_Meth_select_FPKM.txt -c ../../0.RawData/Final/TrainSampleClass.txt -i CoxRegressDiff005Coef.txt -log -o Gene.filter.FPKM.boxplot.txt
/home/lixuefei/Pipeline/Basic/Plot/FrameBoxPlot.py -i Gene.filter.FPKM.boxplot.txt -figsize 10:16 -ylim=-8:5 -o Gene.filter.FPKM.boxplot.pdf -x Key -y Value -huge Class
/home/lixuefei/Pipeline/Basic/TCGA/GetGeneForBoxplot.py -e ../../3.Exp_Meth/Exp_Meth_select_Meth.txt -c ../../0.RawData/Final/TrainSampleClass.txt -i CoxRegressDiff005Coef.txt -o Gene.filter.Meth.boxplot.txt
/home/lixuefei/Pipeline/Basic/Plot/FrameBoxPlot.py -i Gene.filter.Meth.boxplot.txt -figsize 10:16 -ylim=-0.1:1 -o Gene.filter.Meth.boxplot.pdf -x Key -y Value -huge Class
