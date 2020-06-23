#####using DiscovarDeNovo  to assemble the Illumina PE250 reads#####

DiscovarDeNovo   OUT_DIR=asmoutput/  NUM_THREADS=90 READS=A_L1_I307.R1.clean.fastq.gz,A_L1_I307.R2.clean.fastq.gz, A_L2_I308.R1.clean.fastq.gz,A_L2_I308.R2.clean.fastq.gz,B_L1_I307.R1.clean.fastq.gz,B_L1_I307.R2.clean.fastq.gz,B_L2_I308.R1.clean.fastq.gz,B_L2_I308.R2.clean.fastq.gz


###using supernova to assemble the 10XG reads####
supernova-1.1.3/supernova-cs/1.1.3/bin/run --id=RH10x_asm --fastqs=10X-data/ --localcores=90


cd assembly_merging
##perform the assembly_merging pipeline to merge the two assemblies.

