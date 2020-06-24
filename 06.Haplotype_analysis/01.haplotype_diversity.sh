#####Identify the SNPs and InDels between synteny blocks ####


#### preliminarily align two synteny blocks using lastz to get accurate boundary####
###the *.collinear_region.fil.3fold.sim.txt is generated using synteny_block.sh.

z="cds"
for i in {1..12};do
	mkdir $z\_chr$i\_diff
	cd $z\_chr$i\_diff
	mkdir 00_fasta  01_maf
	grep 'chr'$i'_' $z.collinear_region.fil.3fold.sim.txt > chr$i\.collinear_region.fil.3fold.sim.txt
	python2 give_seq_for_lastz.py RH_chr.fa chr$i\.collinear_region.fil.3fold.sim.txt
	python2 create_lastz_maf_shell.py chr$i\.collinear_region.fil.3fold.sim.txt
	sh lastz.sh
	cd ../
done;


for i in {1..12}; do mv cds_chr$i\_diff/*.fa cds_chr$i\_diff/00_fasta  ; done;
for i in {1..12}; do mv cds_chr$i\_diff/*.maf cds_chr$i\_diff/01_maf  ; done;

####re-align blocks to get SNPs and InDels####
z="cds"
for i in {1..12};do
	cd $z\_chr$i\_diff/01_maf
	for  f in *.maf ; do echo "python3.2 ../../filter_maf_chose_best_aln.py "$f $f".flt > "$f".log ">> flt.sh ; done;
	sh flt.sh
	cd ../
	cat 01_maf/*.maf.flt > chr$i.total.maf
	python3.2 ../pair_pos_from_maf.py  chr$i.total.maf  chr$i.lastz.pos
	mkdir 02_diff
	python3.2 ../give_seq_for_lastz_diff.py RH_chr.fa chr$i\.lastz.pos
	python ../create_lastz_diff_shell.py chr$i\.lastz.pos
	sh lastz.2.sh
done;


###collect statistics ###
z="cds"
for i in {1..12};do
	cd $z\_chr$i\_diff
	python3.2 ../lastz_diff_stat.py 02_diff $z\_chr$i\_diff.stat
	echo $z"_chr"$i"_diff.stat.06" >>../$z\_chr_diff.chr.separate.SNP.stat
	echo $z"_chr"$i"_diff.stat.06" >>../$z\_chr_diff.chr.separate.INDEL.stat
	head -1 $z\_chr$i\_diff.stat.06 >> ../$z\_chr_diff.chr.separate.SNP.stat
	head -2 $z\_chr$i\_diff.stat.06 |tail -1 >> ../$z\_chr_diff.chr.separate.INDEL.stat
	cd ../
done;
