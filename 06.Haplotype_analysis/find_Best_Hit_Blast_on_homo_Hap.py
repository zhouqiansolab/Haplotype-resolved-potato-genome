import sys

f1 = open(sys.argv[1])  ##gff file
f2 = open(sys.argv[2])  ##blast out
f3 = open(sys.argv[3],'w')

gene_chr={}
for line in f1:
	line=line.split()
	gene_chr[line[1]]=line[0]
f1.close()

g=''
for line in f2:
	lsp=line.split()
	if lsp[0]==lsp[1]:
		continue
	if lsp[0] !=g and g !='':
		if len(hit_list)==1:   ##only one hit
			f3.write(aln[hit_list[0]])
		else:
			hap0=gene_chr[g]
			hap1=gene_chr[hit_list[0]]
			hap2=gene_chr[hit_list[1]]
			if hap0 !=hap1:  ##if the best hit located on the same chr with the query, then save the second hit
				f3.write(aln[hit_list[0]])
			elif hap0 !=hap2:
				f3.write(aln[hit_list[1]])
			else:
				f3.write(aln[hit_list[0]]) ##if the best and the second hits both located on the same chr with the query, then save the first hit

	if lsp[0] !=g :
		g=lsp[0]; hit_list=[]; aln={}
	if g==lsp[0]:
		if lsp[1] not in aln:
			hit_list.append(lsp[1])
			aln[lsp[1]]=line

if len(hit_list)==1:   ##only one hit
	f3.write(aln[hit_list[0]])
else:
	hap0=gene_chr[g]
	hap1=gene_chr[hit_list[0]]
	hap2=gene_chr[hit_list[1]]
	if hap0 !=hap1:  ##if the best hit located on the same chr with the query, then save the second hit
		f3.write(aln[hit_list[0]])
	elif hap0 !=hap2:
		f3.write(aln[hit_list[1]])
	else:
		f3.write(aln[hit_list[0]]) ##if the best and the second hits both located on the same chr with the query, then save the first hit

f1.close()
f2.close()
