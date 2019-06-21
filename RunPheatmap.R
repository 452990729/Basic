library('pheatmap')

rm(list=ls())
setwd('/home/lixuefei/Project/20190527_Cancer/Fifure1')
dataExpr <- read.table('out.txt', sep='\t', row.names=1, header=T, 
                       quote="", comment="", check.names=F)
dataExpr <- log(dataExpr)
dataExpr_filter <- dataExpr[apply(dataExpr, MARGIN = 1, FUN = function(x) sd(x) != 0),]
pheatmap(dataExpr_filter, scale="row", cluster_cols=TRUE, cluster_rows = TRUE, show_rownames=T, show_colnames=T, border=FALSE, fontsize = 1)

