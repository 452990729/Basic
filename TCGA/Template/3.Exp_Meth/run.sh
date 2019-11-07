/home/lixuefei/Pipeline/Basic/TCGA/SelectMethAndExp.py -exp ../1.DEG/Diff_result.txt -m ../2.meth/MethAnnotation.txt > stats.txt
/home/lixuefei/Pipeline/Basic/ExtractById.py -m ../2.meth/MethSwitchAnno.txt -i Exp_Meth_select.txt -o Exp_Meth_select_Meth.txt
/home/lixuefei/Pipeline/Basic/ExtractById.py -m ../0.RawData/Final/TrainRNAFPKM.txt -i Exp_Meth_select.txt -o Exp_Meth_select_FPKM.txt
/home/lixuefei/Pipeline/Basic/ExtractById.py -m Exp_Meth_select_Meth.txt -i ../0.RawData/Final/TrainCancerClass.txt -o Exp_Meth_select_Meth_Cancer.txt -col
/home/lixuefei/Pipeline/Basic/ExtractById.py -m Exp_Meth_select_FPKM.txt -i ../0.RawData/Final/TrainCancerClass.txt -o Exp_Meth_select_FPKM_Cancer.txt -col
/home/lixuefei/Pipeline/Basic/GroupDataByM.py -c ../0.RawData/Final/TrainCancerClass.txt -i Exp_Meth_select_Meth_Cancer.txt -m median -o Exp_Meth_select_Meth_Cancer_medium.txt -l Methlation
/home/lixuefei/Pipeline/Basic/GroupDataByM.py -c ../0.RawData/Final/TrainCancerClass.txt -i Exp_Meth_select_FPKM_Cancer.txt -m median -o Exp_Meth_select_FPKM_Cancer_medium.txt -l Expression
/home/lixuefei/Pipeline/Basic/MergeData.py -i Exp_Meth_select_FPKM_Cancer_medium.txt,Exp_Meth_select_Meth_Cancer_medium.txt -o Exp_Meth_select_medium.txt
/home/lixuefei/Pipeline/Basic/Plot/ScatterPlot.py -m Exp_Meth_select_medium.txt -diag -ylim=-0.1:1 -xlim=-1:55
Rscript /home/lixuefei/Pipeline/Basic/RNA/enrich.R -f Exp_Meth_select.txt
