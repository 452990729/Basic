#!/usr/bin/env Rscript

library("DESeq2")
library("argparse")


parser <- ArgumentParser(description='Run deseq2 by readscount')
parser$add_argument('-exp', help='the input expression matrix, rows are genes, cols are sampls, requered')
parser$add_argument('-cls', help='the input sample matrix, samples/group, no header, requered')
parser$add_argument('-out', help='output path <<.>>', default='./')
parser$add_argument('-p', help='FDR value cutoff <<0.05>>', default=0.05)
parser$add_argument('-f', help='log foldchange cutoff <<1>>', default=1)
argv <- parser$parse_args()

Exp <- read.table(argv$exp , sep = '\t', row.names=1, header=T,  quote="", comment="", check.names=F)
Sample <- read.table(argv$cls, sep = '\t', row.names=1, header=F,  quote="", comment="", check.names=F)

Exp = Exp[rownames(Sample)]
dds <- DESeqDataSetFromMatrix(Exp, Sample, design= ~ V2)
dds <- DESeq(dds)
res = results(dds)
diff_gene_deseq2 <-subset(res, padj < argv$p & abs(log2FoldChange) > argv$f)
write.table(res,file=paste(argv$out, "All_results.txt", sep="/"), sep = '\t', quote = F, col.names=NA)
write.table(diff_gene_deseq2,file=paste(argv$out, "Diff_result.txt", sep="/"), sep = '\t', quote = F, col.names=NA)
