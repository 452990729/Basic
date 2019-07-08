#!/usr/bin/env Rscript

library('pheatmap')

rm(list=ls())
argv=commandArgs(TRUE)
infile <- argv[1]
if(length(argv)==2) {
        outfile=argv[2]
} else {
        outfile="Heatmap"
}

dataExpr <- read.table(infile, sep='\t', row.names=1, header=T,  quote="", comment="", check.names=F)
#dataExpr <- log(dataExpr)
#dataExpr_filter <- dataExpr[apply(dataExpr, MARGIN = 1, FUN = function(x) sd(x) != 0),]
pdf(paste(outfile, "pdf", sep="."),height = 10,width = 10)
pheatmap(dataExpr, scale="row", cluster_cols=TRUE, cluster_rows = TRUE, show_rownames=T, show_colnames=T, border=FALSE, fontsize = 1)
dev.off()
