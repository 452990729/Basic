/home/lixuefei/Pipeline/Basic/TCGA/GetClinicalForCox.py -c ../5.risk/RiskScore.txt -s ../0.RawData/ClinicalUseful.txt
mkdir univariate
cd univariate
/home/lixuefei/Pipeline/Basic/Survial/CoxSurvial.py -t univariate -s ../../0.RawData/ClinicalUseful.txt -c ../ClinicalForCox.txt
cd ../
mkdir multivariable
cd multivariable
/home/lixuefei/Pipeline/Basic/Survial/CoxSurvial.py -t multivariable -s ../../0.RawData/ClinicalUseful.txt -c ../ClinicalForCox.txt
cd ../
/home/lixuefei/Pipeline/Basic/Survial/CoxForestPlot.py -m multivariable/CoxRegress.txt
/home/lixuefei/Pipeline/Basic/TCGA/NomogramAnalysis.R -m ClinicalForCox.txt -s ../0.RawData/ClinicalUseful.txt
