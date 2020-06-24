####This pipeline is used to align the sequences of RHgv1 to RHgv2 and extract the sequences that can not be properly mapped.

###Use the RHgv1 contigs rather than the scaffolds
python3.2 split_seq_at_NN.py RH_gv1_scaf.fa RH_gv1_contig.fa
python3.2 calculate_len.py -t fa -i RH_gv1_contig.fa -o RH_gv1_contig.fa.len

fasta_make_Nbase_bed.pl RH_gv1_scaf.fa > RH_gv1_scaf.gap.bed

python3.2 contig_agp.py RH_gv1_scaf.fa.len RH_gv1_scaf.gap.bed RH_gv1_contig.agp


### To apply the BLASR, cut the contigs to the fragments with the size of 40 Kb.
python3.2 split_contig.py RH_gv1_contig.fa RH_gv1_contig_40k.fa 40000
python3.2 calculate_len.py -t fa -i RH_gv1_contig.fa -o RH_gv1_contig.fa.len

python3.2 contig_40k_agp.py  RH_gv1_contig.agp  RH_gv1_contig_40k.fa.len RH_gv1_contig_40k.agp

blasr RH_gv1_contig_40k.fa RH_gv2.unitigs.fasta   -m 4 --nproc 20 --out ontctg_ccsutg.m4  --bestn 5 --hitPolicy randombest
python3.2 map_cov.py


###The RHgv1 sequences that are alinged with <90% identity or 50% coverage are extracted and added to RHgv2
python3.2 ./supplemental_ont_asm_seq.py 1>1.log

cat RH_gv2.unitigs.fasta  supplemental_seq_from_RH_gv1_scaf.fa  >RH_whole_contig.fa
