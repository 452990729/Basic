#!/usr/bin/env Rscript

library(limma)
library(argparse)


parser <- ArgumentParser(description='methchip analysis')
parser$add_argument('-i', help='input matrix, col are sample, index are genes')
parser$add_argument('-c', help='input cls file ,no header, col1 is sample col2 is normal/tumor')
parser$add_argument('-fdr', help='fdrFilter value <<0.05>>', type='double', default=0.05)
parser$add_argument('-logFC', help='logFCfilter value <<1>>', type='double', default=1)
argv <- parser$parse_args()

inputFile <- argv$i
class <- argv$c
fdrFilter=argv$fdr
logFCfilter=argv$logFC

outTab <- data.frame()
group=read.table(class, header=F, sep="\t")
Type <- group[,2]
grade <- ifelse(Type=="Normal",1,2)

rt <- read.table(inputFile,sep="\t",header=T,check.names=F)
rt <- as.matrix(rt)
rownames(rt) <- rt[,1]
exp <- rt[,2:ncol(rt)] #行名可被直接移植
dimnames <- list(rownames(exp),colnames(exp))
data <- matrix(as.numeric(as.matrix(exp)),nrow=nrow(exp),dimnames=dimnames)
data=data[,group[,1]]
data <- avereps(data)
data[is.na(data)] <- 0
data <- data[rowMeans(data)>0,]
data <- normalizeBetweenArrays(data)
data=data[!is.na(data[,1]),]
normalData <- cbind(id=row.names(data),data) #为了让id号写入文件
write.table(normalData,file="normalizeMethy.txt",sep="\t",row.names=F,quote=F)

for (i in row.names(data)){
 rt <- rbind(expression=data[i,],grade=grade)
 rt <- as.matrix(t(rt))
 wilcoxTest <- wilcox.test(expression ~ grade, data=rt)

 normalGeneMeans <- mean(data[i,grade==1])
 tumorGeneMeans <- mean(data[i,grade==2])
 logFC <- log2(tumorGeneMeans) - log2(normalGeneMeans)
 pvalue <- wilcoxTest$p.value
 normalMed <- median(data[i,grade==1])
 tumorMed <- median(data[i,grade==2])
 diffMed <- tumorMed - normalMed
 if((( logFC>0) & ( diffMed >0)) | (( logFC < 0 ) & ( diffMed <0 ))){
 outTab <- rbind(outTab,cbind(gene=i,normalMean=normalGeneMeans,TumorMean=tumorGeneMeans,logFC=logFC,pValue=pvalue))
 }}
pValue <- outTab[,"pValue"]
fdr <- p.adjust(as.numeric(as.vector(pValue)),method="fdr")
outTab <- cbind(outTab,fdr=fdr)
write.table(outTab,file="allGene.xls",sep="\t",row.names=F,quote=F)
outDiff <- outTab[(abs(as.numeric(as.vector(outTab$logFC))) > logFCfilter & as.numeric(as.vector(outTab$fdr)) < fdrFilter),]
write.table(outDiff,file="diff.xls",sep="\t",row.names=F,quote=F)

