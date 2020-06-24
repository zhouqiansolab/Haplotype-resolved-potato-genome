author: Qian Zhou  zhouqian_solab@163.com
data: 6/24/2020


The purpose of this pipeline is to analysis the synteny and diversity between two haplotypes of one chromsome.
01.synteny_block.sh    ## First, build the synteny blocks using MCScanX pipeline; then filter the blocks and identify the one-to-one blocks and allelic genes.
02.haplotype_diversity.sh   ##align the synteny blocks using Lastz to identify the variants between blocks.
