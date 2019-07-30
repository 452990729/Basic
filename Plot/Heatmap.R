#!/usr/bin/env Rscript

library(pheatmap)
library(argparse)
library(RColorBrewer)

parser <- ArgumentParser(description='Make Heatmap Plot')
parser$add_argument('-m', help='the input matrix, include header and index')
parser$add_argument('-scale', help='scale data <<row>>', choices=c('row', 'column', 'none'), default='row')
parser$add_argument('-cluster_cols', help='cluster_cols <<TRUE>>', action='store_true')
parser$add_argument('-cluster_rows', help='cluster_rows <<TRUE>>', action='store_true')
parser$add_argument('-show_colnames', help='show_colnames <<TRUE>>', action='store_true')
parser$add_argument('-show_rownames', help='show_rownames <<TRUE>>', action='store_true')
parser$add_argument('-fontsize', help='fontsize <<1>>', type='integer', default=1)
parser$add_argument('-cellwidth', help='size <<NA>>', default='NA')
parser$add_argument('-cellheight', help='size <<NA>>', default='NA')
parser$add_argument('-breakup', help='value <<NA>>', default='NA')
parser$add_argument('-breakdown', help='value <<NA>>', default='NA')
parser$add_argument('-border', help='have border or not <<TRUE>>', action='store_true')
parser$add_argument('-annotation_col', help='annotation_col matrix <<NA>>', default='NA')
parser$add_argument('-annotation_row', help='annotation_rowmatrix <<NA>>', default='NA')
parser$add_argument('-out', help='output file <<HeatmapPlot>>', default='HeatmapPlot')
argv <- parser$parse_args()

ReadData <- function(file_in) {
    data_out <- read.table(file_in, sep='\t', row.names=1, header=T,  quote="", comment="", check.names=FALSE)
    return(data_out)
}

dataExpr <- ReadData(argv$m)
if(argv$annotation_col=='NA') {
    annotation_col <- NA
} else{
    annotation_col <- ReadData(argv$annotation_col)
}
if(argv$annotation_row=='NA') {
        annotation_row <- NA
} else{
        annotation_row <- ReadData(argv$annotation_col)
}
if(argv$cellwidth=='NA') {
    cellwidth <- NA
} else {
    cellwidth <- as.numeric(argv$cellwidth)
}
if(argv$cellheight=='NA') {
    cellheight <- NA
} else {
    cellheight <- as.numeric(argv$cellheight)
}
if(argv$breakup=='NA') {
    bk = NA
} else {
    bk <- unique(c(seq(as.numeric(argv$breakdown),as.numeric(argv$breakup), length=100)))
}

color <- colorRampPalette(c('#436eee', 'white', '#EE0000'))(100)
pdf(paste(argv$out, "pdf", sep="."))
pheatmap_out <- pheatmap(dataExpr, scale=argv$scale, cluster_cols=argv$cluster_cols, cluster_rows = argv$cluster_rows, show_rownames=argv$show_rownames, show_colnames=argv$show_colnames, border=argv$border, fontsize = argv$fontsize, cellwidth = cellwidth, cellheight = cellheight, annotation_row=annotation_row, annotation_col=annotation_col, color=color, breaks=bk)
dev.off()

if(argv$cluster_cols) {
    order_col <- pheatmap_out$tree_col$order
    datat <- data.frame(dataExpr[,order_col], check.names =F)
}
if(argv$cluster_rows) {
    order_row <- pheatmap_out$tree_row$order
    datat <- data.frame(dataExpr[order_row,], check.names =F)
}        

datat <- data.frame(rownames(datat),datat,check.names =F)
colnames(datat)[1] = "ID" 
write.table(datat,file=paste(argv$out, "reorder.txt", sep="_"), row.names=TRUE, quote = FALSE, col.names=NA, sep='\t')
