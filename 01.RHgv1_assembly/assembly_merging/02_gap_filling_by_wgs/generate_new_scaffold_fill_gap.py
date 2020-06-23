
import os
import sys


import Bio
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna


f1=open(sys.argv[1])   ##f1=open('10Xctg_link_by_wgscontig.good.ori')
f2=open(sys.argv[2]) #f2=open('RH_pe250_assembly.fasta')
f3=open(sys.argv[3])  ##f3=open('all.fa.scaf.fa.N.bed')
f4=open(sys.argv[4])  #f4=open('new_10x_ctg.fa')
f5=open(sys.argv[5],'w') #f5=open('RH_10X_new_scaffold.fasta','w')

filled_gap={}; used_contig={}
for line in f1:
	if '#' in line:
		continue
	line=line.split()
	if line[3]=='--':
		if line[1] in filled_gap:
			if filled_gap[line[1]][0] !=line[2] or filled_gap[line[1]][1] !=line[3][0]:  #inconsistent gap information
				print(line[1],'Error1')
			else:  ##save the smaller gap
				if  int(line[5])-int(line[4]) < filled_gap[line[1]][3] -filled_gap[line[1]][2]:
					filled_gap[line[1]]=[line[2],line[3][0],int(line[4]),int(line[5])]
		else:
			filled_gap[line[1]]=[line[2],line[3][0],int(line[4]),int(line[5])]
	else:
		if line[0] in filled_gap:
			if filled_gap[line[0]][0] !=line[2] or filled_gap[line[0]][1] !=line[3][0]:  ## inconsistent gap information
				print(line[0],'Error1')
			else : ##save the smaller gap
				if int(line[5])-int(line[4]) < filled_gap[line[0]][3] -filled_gap[line[0]][2]:
					filled_gap[line[0]]=[line[2],line[3][0],int(line[4]),int(line[5])]
		else:
			filled_gap[line[0]]=[line[2],line[3][0],int(line[4]),int(line[5])]
	used_contig[line[2]]=0
f1.close()

for line in f2:
	if '>' in line and line.split()[0].split('>')[1] in used_contig:
		used_contig[line.split()[0].split('>')[1]]='';  flag=1; name=line.split()[0].split('>')[1]
	elif '>' in line and line.split()[0].split('>')[1] not in used_contig:
		flag=0
	elif '>' not in line and flag:
		used_contig[name]+=line.strip()
f2.close()

raw_gap_size={}; ctg=''
for line in f3:
	line=line.split()
	if line[0] !=ctg:
		ctg=line[0]; flag=1
	if ctg==line[0]:
		raw_gap_size[line[0]+'_'+str(flag)]=(int(line[2])-int(line[1])+1)   ##record the following gap size of each contig
		flag+=1
f3.close()


scaf_name=''
for line in f4:
	if '>' in line:
		tmp_scaf_name=''
		for i in line[1:].split()[0].split('_')[:-1]:
			tmp_scaf_name+=(i+'_')
		tmp_scaf_name=tmp_scaf_name[:-1]; tmp_ctg_name=(line[1:].split()[0])   ##tmp_scaf_name=lg1_1_5 tmp_ctg_name=lg1_1_5_2
		if tmp_scaf_name !=scaf_name and scaf_name != '':
			f5.write('\n')
		if tmp_scaf_name !=scaf_name:
			scaf_name=tmp_scaf_name
			f5.write('>{0}_filled_gap\n'.format(scaf_name))
		if scaf_name==tmp_scaf_name:
			if tmp_ctg_name in filled_gap:
				if -1000 <= (filled_gap[tmp_ctg_name][3] - filled_gap[tmp_ctg_name][2]) <=0:
					gap_content=''
				elif  (filled_gap[tmp_ctg_name][3] - filled_gap[tmp_ctg_name][2]) >0:
					ref_seq=used_contig[filled_gap[tmp_ctg_name][0]][filled_gap[tmp_ctg_name][2]-1:filled_gap[tmp_ctg_name][3]]  ###used_contig[flattened_line_0][2345:4890]
					if filled_gap[tmp_ctg_name][0][1]=='-':
						gap_content=str(Seq(ref_seq,generic_dna).reverse_complement())
					else:
						gap_content=ref_seq
			elif tmp_ctg_name in raw_gap_size:
				gap_content=('N'*raw_gap_size[tmp_ctg_name])
			else:
				gap_content=''
	else :
		f5.write(line.strip()+gap_content)
f5.write('\n')
f4.close()
f5.close()
