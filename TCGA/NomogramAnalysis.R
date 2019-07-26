#!/usr/bin/env Rscript

library(argparse)
library(survival)
library(rms)


parser <- ArgumentParser(description='do nomogram Analysis')
parser$add_argument('-m', help='input matrix ,columns are factors, index are samples')
parser$add_argument('-s', help='input survival matrix , index are sample ,columns include OS and status ')
parser$add_argument('-out', help='output file <<NomogramPlot>>', default='NomogramPlot')
argv <- parser$parse_args()


fl <- read.table(argv$m,sep="\t",header=T,check.names=F, row.names=1)
sur <- read.table(argv$s,sep="\t",header=T,check.names=F, row.names=1)

sur$sample <- rownames(sur)
sur <- sur[,c('OS', 'status', 'sample')]
fl$sample <- rownames(fl)
data <- merge(fl,sur,by.x="sample",by.y="sample",all.x=T)

dd <- datadist(data)
options(datadist="dd")
f <- cph(Surv(OS,status) ~ `RiskScore`+`Tumor stage(III+VI vs. I+II)`+`Age(>= 60 vs. < 60)`
         , data=data, x=TRUE, y=TRUE, surv=TRUE)
survival <- Survival(f)
survival1 <- function(x)survival(365,x)
survival3 <- function(x)survival(1095,x)
survival5 <- function(x)survival(1825,x)

nom <- nomogram(f,fun=list(survival1,survival3,survival5),
                fun.at=c(0.1,seq(0.3,0.7,by=0.2),0.9),
                funlabel=c('1 year survival','3 year survival','5 year survival'))

pdf(paste(argv$out, "pdf", sep="."))
plot(nom)
dev.off()
print(paste('Combined', rcorrcens(Surv(OS,status) ~ predict(f), data = data)[[1]], sep='\t'))
f1 <- cph(Surv(OS,status) ~ `RiskScore`, data=data, x=TRUE, y=TRUE, surv=TRUE)
print(paste('RiskScore', rcorrcens(Surv(OS,status) ~ predict(f1), data = data)[[1]], sep='\t'))

