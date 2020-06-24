#!/public/agis/huangsanwen_group/zhouqian/bin/python3.2


import sys


f1=open(sys.argv[1])   ##input m4 file
f2=open(sys.argv[2])  ##contig agp file
f3=open(sys.argv[3],'w')  ##output file
f3.write('#contig\tchr\tstart\tend\tiden_0.1\tiden_0.9\tiden_0.95\n')


aln={}

for line in f1:
	line=line.split()
	scaf='_'.join(line[0].split('_')[:3])
	iden=line[3]
	map_len= int(line[6])-int(line[5])

	if scaf not in aln:
		aln[scaf]=[]
	aln[scaf].append([iden,map_len])
f1.close()

for line in f2:
	line=line.split()
	if line[0] not in aln:
		f3.write('{0}\t0\t0\t0\n'.format('\t'.join(line)))
	else:
		map_len=[0,0,0]
		for i in aln[line[0]]:
			if float(i[0]) >10:
				map_len[0] += i[1]
			if float(i[0]) >90:
				map_len[1] += i[1]
			if float(i[0]) >95:
				map_len[2] += i[1]
		f3.write('{0}\t{1}\t{2}\t{3}\n'.format('\t'.join(line),map_len[0],map_len[1],map_len[2]))
f3.close()
f2.close()
