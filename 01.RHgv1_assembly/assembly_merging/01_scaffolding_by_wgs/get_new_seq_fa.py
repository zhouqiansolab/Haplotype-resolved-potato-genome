

import Bio
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna


f1=open('all.aln.scaffolding.link.dot')
gap={}
for line in f1:
	if '->' not in line:
		continue
	line=line.split()
	gap_size=int(line[3].split(':')[1])
	if gap_size >0:
		gap[line[0].split('"')[1]+'/'+line[2].split('"')[1]] =gap_size
	else:
		gap[line[0].split('"')[1]+'/'+line[2].split('"')[1]] =0
f1.close()

#wgs_ctg={}
#f1=open('RH_pe250_assembly.fasta')
#name=''
#for line in f1:
#	if '>' in line and line.split()[0][1:] !=name:
#		name=line.split()[0][1:]
#		wgs_ctg[name]=''
#	else:
#		wgs_ctg[name]+=line.strip()
#f1.close()

scaf_10x={}
f1=open('RH_10XG.fasta')
name=''
for line in f1:
	if '>' in line and line.split()[0][1:] !=name:
		name=line.split()[0][1:]
		scaf_10x[name]=''
	else:
		scaf_10x[name]+=line.strip()
f1.close()

flag=1
f2=open('10Xscaf_linked.id')
f3=open('new_10Xscaf_all.fa','w')
for line in f2:
	if len(line.split()[0].split('"'))==3:
		f3.write('>Raw_{0}\t{1} bp\n'.format(flag,line.strip()[1:]))
	else:
		f3.write('>Linked_{0}\t{1} bp\n'.format(flag,line.strip()[1:]))
	flag+=1
	link=line.split()[0].split('"') ###line='>"lg2_1_1858_4871bp"/-_"lg0_17971_1134bp"/-_"lg2_1_541_2149bp"/+_' ; then link=['>', 'lg2_1_1858_4871bp', '/-_', 'lg0_17971_1134bp', '/-_', 'lg2_1_541_2149bp', '/+_']
	for i in range(1,len(link),2):
		scaf_i=''
		for j in link[i].split('_')[:-1]:
			scaf_i+=(j+'_')
		scaf_i=scaf_i[:-1]; scaf_i_seq=scaf_10x[scaf_i]
		if link[i+1][1]=='-':
			scaf_i_seq=str(Seq(scaf_i_seq,generic_dna).reverse_complement())
		gap_content=''
		if i < len(link)-2:
			gap_content= 'N'*(gap[link[i]+'/'+link[i+2]])
		f3.write(scaf_i_seq+gap_content)
		scaf_10x.pop(scaf_i)
	f3.write('\n')
f2.close()
for s in scaf_10x:
	f3.write('>Raw_{0}\t{1} {2} bp\n{3}\n'.format(flag,s,len(scaf_10x[s]),scaf_10x[s]))
	flag+=1
f3.close()
