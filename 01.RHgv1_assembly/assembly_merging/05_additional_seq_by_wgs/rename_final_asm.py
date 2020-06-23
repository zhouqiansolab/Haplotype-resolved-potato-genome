
import os
import sys
import re

removed={}
f1=open('../04_remove_redundancy/removed.scaf.id')
for line in f1:
	removed[line.split()[0]]=0
f1.close()

scaf_lg={}
f1=open('../01_scaffolding_by_wgs/new_10Xscaf_all.id')
for rawline in f1:
	line=rawline.split()
	id =int(line[0].split('_')[1])  ##line[0]='Linked_26'  'Raw_27' 
	if '"' in line[1]:
		ctg1=line[1].split('"')[1].split('_')  ##line[1]="lg3_2_322_5419bp"/-_"lg0_22484_1079bp"/-_"lg0_4063_4523bp"/+_
	else:
		ctg1=line[1].split('_')  ##line[1]=lg0_7654
	if ctg1[0]=='lg0':
		lg='lg0'
	else:
		lg=ctg1[0]+'/'+ctg1[1]
	scaf_lg[id]=[lg,line[0][1:],line[1]]
f1.close()
f2=open('../03_extend_edge_by_wgs/RH_10X_gapfilled_extended_scaf.fa')
f3=open('RH_10XG_WGS_merged.scaf.fa','w')
for line in f2:
	if '>' in line:
		id= int(line.split()[0].split('_')[1])  ### line.split()[0]= Linked_9_filled_gap
		if line.split()[0][1:] in removed:
			flag=0
		else :
			flag=1
			f3.write('>Scaf{0}_{1}\t{2} {3}\n'.format(id,scaf_lg[id][0],scaf_lg[id][1],scaf_lg[id][2]))
	elif '>' not in line and flag:
		f3.write(line)
f2.close()

f2=open('wgs_asm_uniq.1k.fa')  ##this file is generated from wgs_asm_uniq.fa by extracting scaffolds longer than 1kb.
for line in f2:
	if '>' in line:
		id +=1
		f3.write('>Scaf{0}_lg0\t{1}'.format(id,line[1:]))
	else:
		f3.write(line)
f2.close()
f3.close()
