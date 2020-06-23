#!/bin/bash


##scaffolds longer than 20 kb are extracted from RH_10X_gapfilled_extended_scaf.fa to generate RH_scaf_longer.fa.
sawriter RH_scaf_longer.fa.sa RH_scaf_longer.fa

blasr -bestn 10 -m 5 -minMatch 15 -advanceExactMatches 10 -nCandidates 35 -nproc 16 -maxScore -2000 -sa RH_scaf_longer.fa.sa RH_scaf_shorter_20k.fa RH_scaf_longer.fa | cut -d " " -f 1-17 > 10x_redundancy.aln

awk '($4-$3)/$2 >0.90 && $12/($12+$13+$14)>0.999 && $1 != $6 {print $1}' 10x_redundancy.aln > removed.scaf.id  ##these scaffolds may be should put in the gaps of 10x_asm.scaf. but the gaps are filled by the wgs_asm.ctg. so remove these redundant scaffolds
