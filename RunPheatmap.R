library('pheatmap')

rm(list=ls())
setwd('~/Test/')
dataExpr <- read.table('out.txt', sep='\t', row.names=1, header=T, 
                       quote="", comment="", check.names=F)
pheatmap(dataExpr, scale = "row", cluster_cols = TRUE, cluster_rows = FALSE, show_rownames=F, show_colnames=T, border=FALSE,fontsize = 2, cellheight=0)
