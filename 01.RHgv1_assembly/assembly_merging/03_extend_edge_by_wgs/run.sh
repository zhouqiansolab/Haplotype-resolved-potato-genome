
python extend_que_edge.py ../02_gap_filling_by_wgs/10x_wgs.iden95.aln.srtbyref extended_ctg.txt

python generate_new_scaffold_extend_edge.py  ../02_gap_filling_by_wgs/10Xctg_link_by_wgscontig.good.ori RH_pe250_assembly.fasta ../02_gap_filling_by_wgs/new_10Xscaf_all.fa.bed ../02_gap_filling_by_wgs/new_10x_ctg.fa extended_ctg.txt RH_10X_gapfilled_extended_scaf.fa

python ../02_gap_filling_by_wgs/split_seq_at_NN.py RH_10X_gapfilled_extended_scaf.fa  RH_10X_gapfilled_extended_ctg.fa

perl fasta_make_Nbase_bed.pl RH_10X_gapfilled_extended_ctg.fa > RH_10X_gapfilled_extended_ctg.fa.N.bed
