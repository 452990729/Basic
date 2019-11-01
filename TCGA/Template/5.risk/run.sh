/home/lixuefei/Pipeline/Basic/TCGA/MakeRiskScore.py -exp ../4.cox/multivariable/CoxRegressDiff005FPKM.txt -coef ../4.cox/multivariable/CoxRegressDiff005Coef.txt
/home/lixuefei/Pipeline/Basic/TCGA/PlotRiskScore.py -r RiskScore.txt -s ../0.RawData/ClinicalUseful.txt -e ../4.cox/multivariable/CoxRegressDiff005FPKM.txt
/home/lixuefei/Pipeline/Basic/Survial/HighLowGenePlotSurvial.py -s ../0.RawData/ClinicalUseful.txt -e RiskScore.txt -l RiskScore

mkdir ROC
cd ROC
/home/lixuefei/Pipeline/Basic/ML/MlAndPredict.py validator -x ../../4.cox/multivariable/CoxRegressDiff005FPKM.txt -y ../../0.RawData/TCGAStatus.txt
cd ../../
