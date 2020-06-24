aln={}

f1=open('ontctg_ccsutg.m4')
for line in f1:
	line=line.split()
	if line[0] not in aln:
		aln[line[0]]=[line[1],line[3],int(line[6])-int(line[5]),int(line[-1])]  ##aln[que]=[ref,iden,map_len,score]
	else:
		if int(line[-1]) >aln[line[0]][-1] :
			aln[line[0]]=[line[1],line[3],int(line[6])-int(line[5]),int(line[-1])]
f1.close()

f2=open('RH_gv1_contig_40k.fa.len')
f3=open('RH_gv2_contig_40k.map.cov','w')
for line in  f2:
	line=line.split()
	if line[0] not in aln:
		f3.write('{0}\t{1}\t0\t0\t0\n'.format(line[0],line[1]))
	else:
		f3.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(line[0],line[1],aln[line[0]][0],aln[line[0]][1],aln[line[0]][2]))
f3.close()
f2.close()
