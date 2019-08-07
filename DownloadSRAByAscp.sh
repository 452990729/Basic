#!/bin/bash

perl -ne 'chomp;print "~/Software/anaconda2/envs/aspera-3.7.7/bin/ascp -QT -l 100M -i ~/Software/anaconda2/envs/aspera-3.7.7/etc/asperaweb_id_dsa.openssh anonftp\@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/$1/$1$2/$_/$_.sra .\n" if(/^(\w{3})(\d{3})/); ' $1 > ascp.sh

nohup sh ascp.sh &
