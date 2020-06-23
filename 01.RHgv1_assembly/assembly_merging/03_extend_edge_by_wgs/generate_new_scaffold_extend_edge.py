
import os
import sys


import Bio
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna


f1=open(sys.argv[1])   ##f1=open('10Xctg_link_by_wgscontig.good.ori')
f2=open(sys.argv[2]) #f2=open('RH_pe250_assembly.fasta')
f3=open(sys.argv[3])  ##f3=open('all.fa.scaf.fa.N.bed')
f4=open(sys.argv[4])  #f4=open('RH_10XG_assembly.fasta')
f5=open(sys.argv[5]) #f6=open('extended_ctg.txt')
f6=open(sys.argv[6],'w') #f6=open('RH_10X_new_scaffold.fasta','w')

######part I record the extension information of the 10x_contig  ####
extension={}; extension['H'] ={}; extension['T'] ={}
used_contig={}
for line in f5:
	if '#' in line:
		continue
	line=line.split()
	if line[0] not in extension:
		extension[line[0]]={}
	extension[line[2]][line[0]]=[line[1],int(line[3]),int(line[4]),line[5]]  ##extension[T][lg0_15837_1]=[flattened_line_100034,1,858,-]
	used_contig[line[1]]=0
f5.close()

#####part II  record the filling information of the 10x_contig ###
filled_gap={};
#f1=open('10Xctg_link_by_wgscontig.good.ori')
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

####part III record the used WGS_contig  ####
#f2=open('RH_pe250_assembly.fasta')
for line in f2:
	if '>' in line and line.split()[0].split('>')[1] in used_contig:
		used_contig[line.split()[0].split('>')[1]]='';  flag=1; name=line.split()[0].split('>')[1]
	elif '>' in line and line.split()[0].split('>')[1] not in used_contig:
		flag=0
	elif '>' not in line and flag:
		used_contig[name]+=line.strip()
f2.close()

####part IV  record the following raw_gap_content  of 10x_contig###
#f3=open('all.fa.scaf.fa.N.bed')
raw_gap_content={}; ctg=''
for line in f3:
	line=line.split()
	if line[0] !=ctg:
		if ctg+'_'+str(flag) in extension['T']:  ##the last contig of the scaffold
			tail_extension=used_contig[extension['T'][ctg+'_'+str(flag)][0]][extension['T'][ctg+'_'+str(flag)][1]-1:extension['T'][ctg+'_'+str(flag)][2]]   ##used_contig[flattened_line_0][1234:4219]
			if extension['T'][ctg+'_'+str(flag)][3]=='-':
				tail_extension=str(Seq(tail_extension,generic_dna).reverse_complement())
			raw_gap_content[ctg+'_'+str(flag)]= tail_extension
		ctg=line[0]; flag=1   ###don't record the head_extension of the first contig of the scaffold becasue that will influence the codes of writing part.
	if ctg==line[0]:
		tmp_size=(int(line[2])-int(line[1])+1); head_extension=''; tail_extension=''  ##record the following gap size of each contig
		if line[0]+'_'+str(flag) in extension['T']:
			tail_extension=used_contig[extension['T'][line[0]+'_'+str(flag)][0]][extension['T'][line[0]+'_'+str(flag)][1]-1:extension['T'][line[0]+'_'+str(flag)][2]]   ##used_contig[flattened_line_0][1234:4219]
			if extension['T'][line[0]+'_'+str(flag)][3]=='-':
				tail_extension=str(Seq(tail_extension,generic_dna).reverse_complement())
		if line[0]+'_'+str(flag+1) in extension['H']:
			head_extension=used_contig[extension['H'][line[0]+'_'+str(flag+1)][0]][extension['H'][line[0]+'_'+str(flag+1)][1]-1:extension['H'][line[0]+'_'+str(flag+1)][2]]   ##used_contig[flattened_line_0][1234:4219]
			if extension['H'][line[0]+'_'+str(flag+1)][3]=='-':
				head_extension=str(Seq(head_extension,generic_dna).reverse_complement())
		if len(tail_extension)+len(head_extension) <tmp_size:
			raw_gap_content[line[0]+'_'+str(flag)]=(tail_extension+ 'N'*(tmp_size-len(tail_extension)-len(head_extension))+ head_extension)
		else:
			raw_gap_content[line[0]+'_'+str(flag)]= (tail_extension+head_extension)

		flag+=1
###for last one scaffold
if ctg+'_'+str(flag) in extension['T']:  ##the last contig of the scaffold
	tail_extension=used_contig[extension['T'][ctg+'_'+str(flag)][0]][extension['T'][ctg+'_'+str(flag)][1]-1:extension['T'][ctg+'_'+str(flag)][2]]   ##used_contig[flattened_line_0][1234:4219]
	if extension['T'][ctg+'_'+str(flag)][3]=='-':
		tail_extension=str(Seq(tail_extension,generic_dna).reverse_complement())
	raw_gap_content[ctg+'_'+str(flag)]= tail_extension
f3.close()

####partIV  read the raw_10x_ctg and write the new_10x_ctg new_10x_scaf  ### the contigs are in sequential numbers, for example scaf1_1,scaf1_2,scaf1_3,scaf2_1,scaf2_2,scaf2_3,scaf2_4
#f4=open('RH_10XG_assembly.fasta')
#f6=open('RH_10X_new_scaffold.fasta','w')
scaf_name=''
for line in f4:
	if '>' in line:
		tmp_scaf_name=''
		for i in line[1:].split()[0].split('_')[:-1]:
			tmp_scaf_name+=(i+'_')
		tmp_scaf_name=tmp_scaf_name[:-1]; tmp_ctg_name=(line[1:].split()[0])   ##tmp_scaf_name=lg1_1_5 tmp_ctg_name=lg1_1_5_2
		if tmp_scaf_name !=scaf_name and scaf_name != '':
			f6.write('\n')
		if tmp_scaf_name !=scaf_name:
			scaf_name=tmp_scaf_name
			f6.write('>{0}_filled_gap\n'.format(scaf_name))
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
			elif tmp_ctg_name in raw_gap_content:
				gap_content=(raw_gap_content[tmp_ctg_name])
			else:
				gap_content=''
	else :
		f6.write(line.strip()+gap_content)
f6.write('\n')
f4.close()
f6.close()
