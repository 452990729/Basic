/home/lixuefei/Pipeline/Basic/ExtractById.py -m ../0.RawData/Final/TestRNAFPKM.txt -i ../4.cox/multivariable/CoxRegressDiff005.txt -o TestFPKM.txt
/home/lixuefei/Pipeline/Basic/Row2Col.py TestFPKM.txt >tmp
mv tmp TestFPKM.txt
/home/lixuefei/Pipeline/Basic/TCGA/TrimTCGALongID.py -i TestFPKM.txt -row
mv TrimedMatrix.txt TestFPKM.txt

/home/lixuefei/Pipeline/Basic/Survial/CoxSurvial.py -t multivariable -s ../0.RawData/ClinicalUseful.txt -c TestFPKM.txt
#/home/lixuefei/Pipeline/Basic/TCGA/MakeRiskScore.py -exp TestFPKM.txt -coef CoxRegress.txt
/home/lixuefei/Pipeline/Basic/TCGA/MakeRiskScore.py -exp TestFPKM.txt -coef ../4.cox/multivariable/CoxRegressDiff005Coef.txt
/home/lixuefei/Pipeline/Basic/Survial/HighLowGenePlotSurvial.py -s ../0.RawData/ClinicalUseful.txt -e RiskScore.txt -l RiskScore
/home/lixuefei/Pipeline/Basic/TCGA/PlotRiskScore.py -r RiskScore.txt -s ../0.RawData/ClinicalUseful.txt -e TestFPKM.txt

mkdir ROC
cd ROC
/home/lixuefei/Pipeline/Basic/ML/MlAndPredict.py validator -x ../TestFPKM.txt -y ../../0.RawData/TCGAStatus.txt
