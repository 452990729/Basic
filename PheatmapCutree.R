#!/usr/bin/env Rscript

library('pheatmap')
library(argparse)

parser <- ArgumentParser(description='Cut Heatmap')
parser$add_argument('-m', help='the input matrix, include header and index')
parser$add_argument('-scale', help='scale data <<row>>', choices=c('row', 'column', 'none'), default='row')
parser$add_argument('-cutoff', help='fontsize <<2>>', type='integer', default=2)
parser$add_argument('-cut_row', help='cut rows <<TRUE>>', action='store_true')
parser$add_argument('-out', help='output file <<CutTree.txt>>', default='CutTree.txt')
argv <- parser$parse_args()

dataExpr <- read.table(argv$m, sep='\t', row.names=1, header=T, quote="", comment="", check.names=F)

out <- pheatmap(dataExpr, scale=argv$scale, cluster_cols=TRUE, cluster_rows = TRUE)

row_cluster=cutree(out$tree_row,k=argv$cutoff)
col_cluster=cutree(out$tree_col,k=argv$cutoff)
if(argv$cut_row) {
    write.table(row_cluster, file = argv$out, sep='\t', row.names =TRUE, quote = FALSE, col.names=NA)
} else{
    write.table(col_cluster, file = argv$out, sep='\t', row.names =TRUE, quote = FALSE, col.names=NA)
}
file.remove('Rplots.pdf')

