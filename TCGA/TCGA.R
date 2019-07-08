
library(TCGAbiolinks)
library(dplyr)
library(SummarizedExperiment)
library(argparse)

argv=commandArgs(TRUE)
parser <- ArgumentParser(description='download data from TCGA')
parser$add_argument('-t', help='the cancer type, seperate by :,exsample BRCA:GBM. Cancer list<"BRCA","GBM","OV","LUAD","UCEC","KIRC","HNSC","LGG","THCA","LUSC","PRAD","SKCM","COAD","STAD","BLCA","LIHC","CESC","KIRP","SARC","LAML","ESCA","PAAD","PCPG","READ","TGCT","THYM","KICH","ACC","MESO","UVM","DLBC","UCS","CHOL">')
parser$add_argument('-c', help='download type <RNASeq, miRNA, CNV, meth, clinical>', default='clinical')
argv <- parser$parse_args()

#下面填入要下载的癌症种类
request_cancer=unlist(strsplit(argv$t, split=':'))
content=unlist(strsplit(argv$c, split=':'))

for (i in request_cancer) {
  cancer_type=paste("TCGA",i,sep="-")
  print(cancer_type)

  if ("clinical" %in% content) {
  #下载临床数据
  clinical <- GDCquery_clinic(project = cancer_type, type = "clinical")
  write.table(clinical,file = paste(cancer_type,"clinical.txt",sep = "-"),sep = "\t",quote = FALSE,col.names=NA)
  }
  if ("RNASeq" %in% content) {
  #下载rna-seq的counts数据
  query <- GDCquery(project = cancer_type, 
                    data.category = "Transcriptome Profiling", 
                    data.type = "Gene Expression Quantification", 
                    workflow.type = "HTSeq - FPKM")
  
  GDCdownload(query, method = "api", files.per.chunk = 100)
  expdat <- GDCprepare(query = query)
  count_matrix=assay(expdat)
  write.table(count_matrix,file = paste(cancer_type,"RNAFPKM.txt",sep = "-"),sep = "\t",quote = FALSE,col.names=NA)
  }
  if ("miRNA" %in% content) {
  #下载miRNA数据
  query <- GDCquery(project = cancer_type, 
                    data.category = "Transcriptome Profiling", 
                    data.type = "miRNA Expression Quantification")
#                    workflow.type = "BCGSC miRNA Profiling")
  
  GDCdownload(query, method = "api", files.per.chunk = 50)
  expdat <- GDCprepare(query = query)
#  count_matrix=assay(expdat)
  write.table(expdat,file = paste(cancer_type,"miRNA.txt",sep = "-"),sep = "\t",quote = FALSE,col.names=NA)
  }
  if ("CNV" %in% content) {
  #下载Copy Number Variation数据
  query <- GDCquery(project = cancer_type, 
                    data.category = "Copy Number Variation", 
                    data.type = "Copy Number Segment")
  
  GDCdownload(query, method = "api", files.per.chunk = 50)
  expdat <- GDCprepare(query = query)
#  count_matrix=assay(expdat)
  write.table(expdat,file = paste(cancer_type,"Copy-Number-Variation.txt",sep = "-"),sep = "\t",quote = FALSE,col.names=NA)
  }
  if ("meth" %in% content) {
  #下载甲基化数据
  query.met <- GDCquery(project =cancer_type,
                        legacy = TRUE,
                        data.category = "DNA methylation")
  GDCdownload(query.met, method = "api", files.per.chunk = 300)
  expdat <- GDCprepare(query = query)
#  count_matrix=assay(expdat)
  write.table(expdat,file = paste(cancer_type,"methylation.txt",sep = "-"),sep = "\t",quote = FALSE,col.names=NA)
  }
}
