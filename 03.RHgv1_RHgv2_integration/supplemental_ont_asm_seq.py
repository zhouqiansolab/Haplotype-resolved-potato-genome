
seq={}
f1=open('RH_gv1_contig_40k.map.cov')
for line in f1:
	line=line.split()
	if float(line[3]) <90 or int(line[4])/int(line[1]) <0.5:
		seq[line[0]]=0
f1.close()

chr={}
f2=open('RH_gv1_contig_40k.agp')
for line in f2:
	if '#' in line[0]:
		continue
	line=line.split()
	if line[0] in seq:
		if line[4] not in chr:
			chr[line[4]]=[]
		chr[line[4]].append([int(line[5]),int(line[6])])
		print("ok1",line[4],line[5],line[6])
f2.close()


for c in chr:
	tmp_pos=[]
	start=chr[c][0][0]; end=chr[c][0][1]
	if len(chr[c])>1:
		for i in range(1,len(chr[c])):
			if chr[c][i][0] - end <=2000:
				end=chr[c][i][1]  ##the two fragments that distance less than 2kb are merged
			else:
				tmp_pos.append([start,end])
				start=chr[c][i][0]
				end=chr[c][i][1]
	tmp_pos.append([start,end])
	chr[c]=tmp_pos  ##update the positions
	for i in tmp_pos:
		print("ok2",c,i[0],i[1])


f4=open('RH_gv1_scaf.fa')
f5=open('supplemental_seq_from_RH_gv1_scaf.fa','w')
chr_seq={}
chr_name=''
for line in f4:
	if '>' in line[0] and chr_name !='':
		chr_seq[chr_name]=seq
	if '>' in line[0]:
		seq=''
		chr_name=line.split()[0][1:]
	else:
		seq+=line.strip()
f4.close()

flag=1
for i in range(1,13):
	for j in range(1,3):
		c='chr'+str(i)+'_'+str(j)
		for pos in chr[c]:
			if pos[1]-pos[0] >1000:
				f5.write('>ontctg{0}\t{1}\t{2}-{3}\n{4}\n'.format(flag,c,pos[0],pos[1],chr_seq[c][pos[0]-1:pos[1]]))
				flag+=1
		chr.pop(c)
for c in chr:
	for pos in chr[c]:
		if pos[1]-pos[0] >1000:
			f5.write('>ontctg{0}\t{1}\t{2}-{3}\n{4}\n'.format(flag,c,pos[0],pos[1],chr_seq[c][pos[0]-1:pos[1]]))
			flag +=1
f5.close()


f2=open('supplemental_seq_from_RH_gv1_scaf.fa')
f3=open('RH_gv1_gene.gff3') ###To avoid breaking the annotated genes when extract the sequences.
f4=open('supplemental_gene_from_RH_gv1.gff3','w')
f4.write('\n')

agp={}
for line in f2:
	if '>' in line[0]:
		line=line.split()
		if line[1] not in agp:
			agp[line[1]]=[]
		pos0=int(line[2].split('-')[0])
		pos1=int(line[2].split('-')[1])
		agp[line[1]].append([line[0][1:],pos0,pos1])
f2.close()

flag=0
for line in f3:
	lsp=line.split()
	if len(lsp) ==0 and flag:
		f4.write('\n')
	if len(lsp) ==0:
		flag=0; info=[]
	elif len(lsp) >0 and 'gene'==lsp[2] and lsp[0] in agp:
		for pos in agp[lsp[0]]:
			if pos[1] <= int(lsp[3]) <=pos[2] and  pos[1] <= int(lsp[4]) <=pos[2] :  ##only when the gene is fully involved in the interval.
				print('gene',line)
				info=pos
				flag=1
				break
	if  len(lsp) >0 and flag:
		start=int(lsp[3]) - pos[1] +1
		end=int(lsp[4]) - pos[1] +1
		if start * end <1:
			print('error',pos,line)
		f4.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(pos[0],lsp[1],lsp[2],start,end,'\t'.join(lsp[5:])))
f4.close()
