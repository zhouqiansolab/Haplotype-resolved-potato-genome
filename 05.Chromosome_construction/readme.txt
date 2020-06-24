author: Qian Zhou  zhouqian_solab@163.com
data: 6/24/2020


############ Commands for Hi-C Pro and ALLHiC pipeline ############
##The ALLHIC tools are download from https://github.com/tangerzhang/ALLHiC. Please cite Zhang, X. Zhang, S. Zhao, Q. Ming, R. Tang, H. Assembly of allele-aware, chromosomal scale autopolyploid genomes based on Hi-C data. Nature Plants, doi:10.1038/s41477-019-0487-8 (2019).


##The input files hap1.fa and hap2.fa including the contigs that are phased through genetic grouping.
##Extract the contigs belonging to lg1_1, lg2_1, lg3_1 ....lg12_1 to generate hap1.fa
##Extract the contigs belonging to lg1_2, lg2_2, lg3_2 ....lg12_2 to generate hap1.fa


###The pipeline for haplotype 1#####
#Build index
/software/bowtie2-2.2.9/bowtie2-build hap1.fa hap1
#Digest genome
/software/HiC-Pro-2.11.1/bin/utils/digest_genome.py -r ^GATC -o hap1.MboI.bed ccs_asm.unitigs.fasta
#Align Hi-C reads to the assembly
/software/HiC-Pro_2.11.1/bin/HiC-Pro -i data -o outdir_hap1 -c config-hicpro.txt

#use hap1.bwt2pairs.bam for ALLHiC pipeline
export PATH=/software/ALLHIC-master/bin: /software/ALLHIC-master/scripts:$PATH
PreprocessSAMs.pl hap1.bwt2pairs.bam hap1.fa MBOI
ln -s hap1.bwt2pairs.REduced.paired_only.bam clean.bam
allhic extract clean.bam hap1.fa --RE GATC
ALLHiC_rescue -b clean.bam -m 0.1 -r hap1.fa -c hap1.cluster -i clean.counts_GATC.txt
for i in {1..12};do allhic optimicze group$i.txt clean.clm;done
ALLHiC_build hap1.fa
ALLHiC_plot clean.bam groups.agp groups.asm.fasta.len 500k pdf
mv groups.asm.fasta hap1.groups.asm.fasta

###The pipeline for haplotype 2#####
#Build index
/software/bowtie2-2.2.9/bowtie2-build hap2.fa hap2
#Digest genome
/software/HiC-Pro-2.11.1/bin/utils/digest_genome.py -r ^GATC -o hap2.MboI.bed ccs_asm.unitigs.fasta
#Align Hi-C reads to the assembly
/software/HiC-Pro_2.11.1/bin/HiC-Pro -i data -o outdir_hap2 -c config-hicpro.txt

#use hap2.bwt2pairs.bam for ALLHiC pipeline
export PATH=/software/ALLHIC-master/bin: /software/ALLHIC-master/scripts:$PATH
PreprocessSAMs.pl hap2.bwt2pairs.bam hap2.fa MBOI
ln -s hap2.bwt2pairs.REduced.paired_only.bam clean.bam
allhic extract clean.bam hap2.fa --RE GATC
ALLHiC_rescue -b clean.bam -m 0.1 -r hap2.fa -c hap2.cluster -i clean.counts_GATC.txt
for i in {1..12};do allhic optimicze group$i.txt clean.clm;done
ALLHiC_build hap2.fa
ALLHiC_plot clean.bam groups.agp groups.asm.fasta.len 500k pdf
mv groups.asm.fasta hap2.groups.asm.fasta

cat hap1.groups.asm.fasta hap2.groups.asm.fasta > whole.genome.chr.fasta

###For the whole diploid genome####
cat hap1.fa hap2.fa > whole.genome.scaf.fasta
bowtie2-build whole.genome.scaf.fasta whole.genome.scaf.fasta
/software/HiC-Pro-2.11.1/bin/utils/digest_genome.py   -r ^GATC -o whole.genome.scaf.MboI.bed whole.genome.scaf.fasta
/software/HiC-Pro_2.11.1/bin/HiC-Pro -i data   -o whole_genome_scaf -c whole_genome_scaf_hicpro.config
PreprocessSAMs.pl whole.genome.scaf.fasta.bwt2pairs.bam whole.genome.scaf.fasta  MBOI
ln -s whole.genome.scaf.fasta.bwt2pairs.REduced.paired_only.bam  whole.clean.bam
ALLHiC_plot whole.clean.bam All_chr_4_hicplot.agp chr.len   500k pdf
