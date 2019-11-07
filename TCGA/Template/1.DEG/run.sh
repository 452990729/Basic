/home/lixuefei/Pipeline/Basic/RNA/DiffAnalysis/RunDeseq2.R -exp ../0.RawData/Final/TrainRNACount.txt -cls ../0.RawData/Final/TrainSampleClass.txt
/home/lixuefei/Pipeline/Basic/RNA/ExtractById.py -m ../0.RawData/Final/TrainRNAFPKM.txt -i Diff_result.txt -o Diff_result_FPKM.txt
/home/lixuefei/Pipeline/Basic/Plot/Heatmap.R -m Diff_result_FPKM.txt -scale column -cluster_cols -cluster_rows -fontsize 10 -annotation_col ../0.RawData/Final/TrainSampleClass.txt -breakup=1 -breakdown=-1
