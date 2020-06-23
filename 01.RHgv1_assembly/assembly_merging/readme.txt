author: Qian Zhou  zhouqian_solab@163.com
data: 10/29/2019



This pipeline was built in the project resolving the genome of a diploid potato. The purpose of this pipeline is to merge the assemblies generated from WGS sequencing and 10XG sequencing.
When run the pipeline, the scripts in each directory will be executed sequentially.
The Python(3.2+), Perl, BLASR are required. Please note that the aligning parameters in scripts are based on BLASR v1.3.1. If latest BLASR was used, please update the command lines.


01_scaffolding_by_wgs   # The contigs of WGS assembly were took as accurate long reads to scaffold the 10XG assembly.
02_gap_filling_by_wgs   # The contigs of WGS assembly were took as accurate long reads to fill the gaps in 10XG scaffolds.
03_extend_edge_by_wgs   # If the WGS contigs are mapped at the end of single 10XG scaffold, the 10XG scaffold will be extended by WGS contigs.
04_remove_redundancy    # Remove the redundant sequences in the two assemblies.
05_additional_seq_by_wgs  #The WGS contigs that can not be aligned to any 10XG scaffold are added into the merged assembly.
