#!/usr/bin/env Rscript

library(biomaRt)
library(argparse)

parser <- ArgumentParser(description='convert spe gene symbol to mouse gene symbol')
parser$add_argument('-m', help='the input matrix, include header and index')
parser$add_argument('-out', help='output file <<Trasformed.txt>>', default='Trasformed.txt')
argv <- parser$parse_args()

ReadData <- function(file_in) {
    data_out <- read.table(file_in, sep='\t', row.names=1, header=T,  quote="", comment="", check.names=FALSE)
    data_out <- as.matrix(data_out)
    return(data_out)
}

convertMouseGeneList <- function(x){

     require("biomaRt")

     human = useMart("ensembl", dataset = "hsapiens_gene_ensembl")

     mouse = useMart("ensembl", dataset = "mmusculus_gene_ensembl")

     genesV2 = getLDS(attributes = c("mgi_symbol"),

                       filters = "mgi_symbol",

                       values = x , mart = human,

                       attributesL = c("hgnc_symbol"),

                       martL = mouse, uniqueRows=T)

     #humanx <- unique(genesV2[, 2])

     # Print the first 6 genes found to the screen

     #print(head(genes))

     return(genesV2)

}
data_out <- ReadData(argv$m)
row_name <- as.vector(rownames(data_out))
ctl_name <- convertMouseGeneList(genes)
outTab <- cbind(data_out,gene_name=ctl_name)
write.table(outDiff,file=argv$out,sep="\t",row.names=F,quote=F)
