#!/PROJECT/home/lixuefei/Software/anaconda2/envs/bioconductor-illuminahumanmethylation450kanno-0.6.0/bin/Rscript

library(argparse)
library("IlluminaHumanMethylation450kanno.ilmn12.hg19")

parser <- ArgumentParser(description='convert meth id to gene id')
parser$add_argument('-m', help='input matrix ,columns gene are meth id')
parser$add_argument('-o', help='output file<<MethAnnotation.txt>>', default='MethAnnotation.txt')
argv <- parser$parse_args()

data(IlluminaHumanMethylation450kanno.ilmn12.hg19)
annotation.table = getAnnotation(IlluminaHumanMethylation450kanno.ilmn12.hg19)
annotation.table$gene=rownames(annotation.table)
annotation.table=annotation.table[,c("gene","UCSC_RefGene_Name")]

meth <- read.table(argv$m, sep="\t",header=T,check.names=F)

mergeRes=merge(meth,annotation.table,by.x="id",by.y="gene",all.x=T)
write.table(mergeRes, file=argv$o, sep='\t', row.names=F, col.names=T, quote=F)
