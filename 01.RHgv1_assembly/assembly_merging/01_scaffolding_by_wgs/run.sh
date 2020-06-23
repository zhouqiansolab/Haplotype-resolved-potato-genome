#!/bin/bash


sawriter RH_10XG_assembly.fasta.sa RH_10XG_assembly.fasta
blasr -bestn 10 -m 5 -minMatch 15 -advanceExactMatches 10 -nCandidates 35 -nproc 5 -maxScore -2000 -sa RH_10XG_assembly.fasta.sa  RH_pe250_assembly.fasta  RH_10XG_assembly.fasta | cut -d " " -f 1-17 > wgs_10X.aln

awk '$12/($12+$13+$14) >=0.95' wgs_10X.aln > wgs_10X.iden95.aln
python correct_que_pos.py wgs_10X.iden95.aln wgs_10X.iden95.aln.corrpos
python sort_aln_byref.py wgs_10X.iden95.aln.corrpos wgs_10X.iden95.aln.corrpos.srtbyref
python chos_best_aln_for_ref.py wgs_10X.iden95.aln.corrpos.srtbyref wgs_10X.iden95.aln.corrpos.srtbyref.flt
python sort_aln_byque.py wgs_10X.iden95.aln.corrpos.srtbyref.flt wgs_10X.iden95.srtbyque


python ref_covered_by_single_que.py wgs_10X.iden95.srtbyque 10Xscaf_link_by_wgscontig.txt
python filter_link.py 10Xscaf_link_by_wgscontig.txt 10Xscaf_link_by_wgscontig.flt 10Xscaf_link_by_wgscontig.dot2
python solve_BOG.py 10Xscaf_link_by_wgscontig.dot2 10Xscaf_linked.id 1>solve_BOG.log
python get_new_seq_fa.py
