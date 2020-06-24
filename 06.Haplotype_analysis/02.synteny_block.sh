######This pipeline is used to identify the homologous regions and allelic genes between two haplotypes  ####


###get primary collinearity using MCScanX ###

 z='RH_gene'
makeblastdb  -in  $z.cds.fa -input_type fasta  -dbtype nucl -out $z -logfile makeblastdb.log
blastn -db $z -query $z.cds.fa -out $z.blast -evalue 1e-5 -outfmt 6 -num_threads 9
awk '$1 != $2'  $z.blast >>00 && mv 00 RH_20200227_gene.blast
awk '$3=="gene"{split($9,a,";"); print $1"\t"substr(a[1],4,100)"\t"$4"\t"$5}' $z.gff3 > $z.blast.gff
python3.2 ./find_Best_Hit_Blast_on_homo_Hap.py   $z.blast.gff $z.blast $z.candidate.blast

python ./attriubte_species_to_gene_name.py $z.blast.gff $z.candidate.blast $z.mcscanx.blast $z.mcscanx.gff

MCScanX -s 4 -a $z.mcscanx

####identify the one-to-one synteny blocks bewteen two haplotypes of one chromosome ####

python2 add_pos_to_collinearity.py $z.gff $z.collinearity $z.collinearity.pos
python2 format_pos_file.py $z.collinearity.pos $z.collinearity.mod.pos
mv $z.collinearity.mod.pos $z.collinearity.pos
grep 'Alignment'  $z.collinearity.pos  >$z.collinear_region.txt
sort -k 10,10 -k 11n,11 $z.collinear_region.txt >00
mv 00 $z.collinear_region.txt
python2 ./filter_collinear_region.py $z.collinear_region.txt $z.collinear_region.fil.txt $z.collinear_region.nonortho_block.txt> $z.collinear_region.fil.3fold.txt
awk '{print $1" "$3"\t"$6"\t"$10"\t"$11"\t"$14"\t"$16"\t"$18"\t"$19"\t"$22"\t"$24"\t"$8}' $z.collinear_region.fil.3fold.txt >$z.collinear_region.fil.3fold.sim.txt

python3.2 ./get_gene_pair.py  $z.collinear_region.fil.3fold.txt $z.gff $z.collinearity  collinear_gene_pair
