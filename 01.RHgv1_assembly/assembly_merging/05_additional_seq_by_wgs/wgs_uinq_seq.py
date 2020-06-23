

import sys


f1=open(sys.argv[1])   ##wgs_asm_ctg and 10x_asm_ctg alignment file. ##wgs_asm_ctg is the reference
f2=open(sys.argv[2])   ###wgs_asm_ctg is the query
f3=open(sys.argv[3])   ## RH_pe250_assembly.fasta
f4=open(sys.argv[4],'w')  ##output wgs_asm_ctg unique seq

mapped_wgs={}
for line in f1:
	mapped_wgs[line.split()[5]]=0
f1.close()
for line in f2:
	mapped_wgs[line.split()[0]]=0
f2.close()
for line in f3:
	if '>' in line and line.split()[0][1:]  not in mapped_wgs:
		f4.write(line)
		flag=1
	if  '>' in line and line.split()[0][1:]  in mapped_wgs:
		flag=0
	elif '>' not in line and flag:
		f4.write(line)
f2.close()
f3.close()
