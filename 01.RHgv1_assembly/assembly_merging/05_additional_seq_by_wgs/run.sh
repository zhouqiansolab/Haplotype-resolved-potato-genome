#!/bin/bash


python wgs_uinq_seq.py ../02_gap_filling_by_wgs/10x_wgs.iden95.aln.srtbyref ../01_scaffolding_by_wgs/all.aln.srtbyref.flt RH_pe250_assembly.fasta  wgs_asm_uniq.fa
python rename_final_asm.py
