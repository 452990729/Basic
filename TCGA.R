# if (!requireNamespace("BiocManager", quietly=TRUE))
#   install.packages("BiocManager")
# BiocManager::install("TCGAbiolinks")
 

library(TCGAbiolinks)
library(dplyr)
library(DT)
library(SummarizedExperiment)


#下面填入要下载的癌症种类
request_cancer=c("PRAD","BLCA","KICH","KIRC","KIRP")
for (i in request_cancer) {
  cancer_type=paste("TCGA",i,sep="-")
  print(cancer_type)
  #下载临床数据
  clinical <- GDCquery_clinic(project = cancer_type, type = "clinical")
  write.csv(clinical,file = paste(cancer_type,"clinical.csv",sep = "-"))
  
  #下载rna-seq的counts数据
  query <- GDCquery(project = cancer_type, 
                    data.category = "Transcriptome Profiling", 
                    data.type = "Gene Expression Quantification", 
                    workflow.type = "HTSeq - Counts")
  
  GDCdownload(query, method = "api", files.per.chunk = 100)
  expdat <- GDCprepare(query = query)
  count_matrix=assay(expdat)
  write.csv(count_matrix,file = paste(cancer_type,"Counts.csv",sep = "-"))
  
  #下载miRNA数据
  query <- GDCquery(project = cancer_type, 
                    data.category = "Transcriptome Profiling", 
                    data.type = "miRNA Expression Quantification", 
                    workflow.type = "BCGSC miRNA Profiling")
  
  GDCdownload(query, method = "api", files.per.chunk = 50)
  expdat <- GDCprepare(query = query)
  count_matrix=assay(expdat)
  write.csv(count_matrix,file = paste(cancer_type,"miRNA.csv",sep = "-"))
  
  #下载Copy Number Variation数据
  query <- GDCquery(project = cancer_type, 
                    data.category = "Copy Number Variation", 
                    data.type = "Copy Number Segment")
  
  GDCdownload(query, method = "api", files.per.chunk = 50)
  expdat <- GDCprepare(query = query)
  count_matrix=assay(expdat)
  write.csv(count_matrix,file = paste(cancer_type,"Copy-Number-Variation.csv",sep = "-"))
  
  #下载甲基化数据
  query.met <- GDCquery(project =cancer_type,
                        legacy = TRUE,
                        data.category = "DNA methylation")
  GDCdownload(query.met, method = "api", files.per.chunk = 300)
  expdat <- GDCprepare(query = query)
  count_matrix=assay(expdat)
  write.csv(count_matrix,file = paste(cancer_type,"methylation.csv",sep = "-"))
}
