#!/usr/bin/env Rscript
library("clusterProfiler")      
library("topGO")                 
library("Rgraphviz")         
library("pathview")                
library("org.Hs.eg.db")
library("argparse")

parser <- ArgumentParser(description='Run deseq2 by readscount')
parser$add_argument('-f', help='the input gene file, col1 is gene, , requered')
parser$add_argument('-out', help='output path <<./Enrich>>', default='./Enrich')
parser$add_argument('-type', help='gene name type SYMBOL, ENSEMBL, REFSEQ<<SYMBOL>>', default='SYMBOL')
argv <- parser$parse_args()

result=read.table(argv$f, sep="\t", header=F, quote="", comment="", check.names=F)

outdir=argv$out
if(file.exists(outdir)) {
    setwd(outdir)
} else {
    dir.create(outdir)
    setwd(outdir)
}

genes=as.character(result$V1)
genetype=argv$type

entrez_id=mapIds(x=org.Hs.eg.db,keys=genes,keytype=genetype,column ="ENTREZID")
entrez_id=na.omit(entrez_id)
erich.go.ALL=enrichGO(gene=entrez_id,OrgDb=org.Hs.eg.db,keyType="ENTREZID",ont="ALL",pvalueCutoff=0.05,qvalueCutoff=0.05)
write.table(summary(erich.go.ALL),paste(basename(outdir), ".G-enrich.txt", sep=""), row.names =F, sep = '\t', quote = F)
pdf(paste(basename(outdir), ".G-enrich.pdf", sep=""),height = 10,width = 10)
barplot(erich.go.ALL,drop=TRUE,showCategory = 25)
dev.off()
KEGG=enrichKEGG(gene=entrez_id,pvalueCutoff=0.05,qvalueCutoff=0.1)
write.table(summary(KEGG),paste(basename(outdir), ".K-enrich.txt", sep=""), row.names =F, sep = '\t', quote = F)
pdf(paste(basename(outdir), ".K-enrich.pdf", sep=""), height = 10,width = 10)
dotplot(KEGG,showCategory = 12) 
dev.off()
