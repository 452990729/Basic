Rscript /home/lixuefei/Pipeline/Basic/Meth/TCGAMeth.R -i ../0.RawData/Final/TrainMeth.txt -c ../0.RawData/Final/TrainSampleClass.txt
Rscript /home/lixuefei/Pipeline/Basic/Meth/Meth2Gene.R -m diff.xls -o MethAnnotation.txt
/home/lixuefei/Pipeline/Basic/TCGA/GetMethFromAnno.py ../0.RawData/Final/TrainMeth.txt MethAnnotation.txt
/home/lixuefei/Pipeline/Basic/Plot/Heatmap.R -m MethSwitchAnno.txt -scale column -cluster_cols -cluster_rows -fontsize 10 -annotation_col ../0.RawData/Final/TrainSampleClass.txt -breakup=1 -breakdown=-1
