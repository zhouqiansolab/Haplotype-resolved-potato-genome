###### Assemble the HiFi reads using CANU #####

####### Commands for canu assembly ############

#generate HiFi reads from subreads.bam
/software/smrtlink/smrtcmds/bin/ccs -j 48 subreads.bam > ccs.bam
/software/samtools-1.9/bin/samtools/samtools fasta -@ 48 ccs.bam > ccs.reads.fa

###assembly by canu with the following command, genomeSize were pre-estimated by k-mer analysis:
/software/canu-1.9/Linux-amd64/bin/canu -assemble -p ccs_asm genomeSize=1600m maxThreads=48 -pacbio-hifi ccs.reads.fa

###canu output two assembles, ccs_asm.contigs.fasta and ccs_asm.unitigs.fasta. We chose ccs_asm.unitigs.fasta for downstream analysis
