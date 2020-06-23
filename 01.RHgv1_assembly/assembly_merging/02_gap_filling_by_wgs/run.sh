
perl fasta_make_Nbase_bed.pl ../01_scaffolding_by_wgs/new_10Xscaf_all.fa > new_10Xscaf_all.fa.bed
python split_seq_at_NN.py ../01_scaffolding_by_wgs/new_10Xscaf_all.fa new_10x_ctg.fa

sawriter RH_pe250_assembly.fasta.sa RH_pe250_assembly.fasta
blasr -bestn 10 -m 5 -minMatch 15 -advanceExactMatches 10 -nCandidates 35 -nproc 6 -maxScore -2000 -sa RH_pe250_assembly.fasta.sa new_10x_ctg.fa   RH_pe250_assembly.fasta | cut -d " " -f 1-17 > 10x_wgs.aln

awk '$12/($12+$13+$14) >=0.95' 10x_wgs.aln > 10x_wgs.iden95.aln
python ../01_scaffolding_by_wgs/sort_aln_byque.py 10x_wgs.iden95.aln 10x_wgs.iden95.aln.srtbyque
python chos_best_aln_for_que.py 10x_wgs.iden95.aln.srtbyque  10x_wgs.iden95.aln.flt
python ../01_scaffolding_by_wgs/sort_aln_byref.py 10x_wgs.iden95.aln.flt 10x_wgs.iden95.aln.srtbyref
python gap_filling_link_by_ref.py 10x_wgs.iden95.aln.srtbyref 10Xctg_link_by_wgscontig.good.ori 10Xctg_link_by_wgscontig.bad.ori
python generate_new_scaffold_fill_gap.py  10Xctg_link_by_wgscontig.good.ori RH_pe250_assembly.fasta  new_10Xscaf_all.fa.bed new_10x_ctg.fa RH_10X_gapfilled_scaf.fa

perl fasta_make_Nbase_bed.pl RH_10X_gapfilled_ctg.fa > RH_10X_gapfilled_ctg.fa.N.bed
