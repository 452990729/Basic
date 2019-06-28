library('pheatmap')
argv=commandArgs(TRUE)
infile <- argv[1]
outfile <- argv[2]
cufoff <- argv[3]

dataExpr <- read.table(infile, sep='\t', row.names=1, header=T, quote="", comment="", check.names=F)

out <- pheatmap(dataExpr, scale="none", cluster_cols=TRUE, cluster_rows = TRUE, show_rownames=T, show_colnames=T, border=FALSE, fontsize = 1)

row_cluster=cutree(out$tree_row,k=cufoff)
#newOrder=dataExpr[out$tree_row$order,]
#newOrder[,ncol(newOrder)+1]=row_cluster[match(rownames(newOrder),names(row_cluster))]
#colnames(newOrder)[ncol(newOrder)]="Cluster"


write.table(row_cluster, file = outfile, sep='\t', row.names =TRUE, quote = FALSE, col.names=NA)
file.remove('Rplots.pdf')

