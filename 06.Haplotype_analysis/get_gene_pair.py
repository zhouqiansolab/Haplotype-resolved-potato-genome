import sys

f1=open(sys.argv[1])   ##reliable block
block={}
for line in f1:
	if '## Alignment' in line:
		block[line.split(':')[0]]=0
f1.close()

f2=open(sys.argv[2])  ##gff file
gene={}
for line in f2:
	line=line.split()
	gene[line[1]]=[line[0],line[2],line[3]]
f2.close()


f3=open(sys.argv[3])  ##collinearity file
f4=open(sys.argv[4],'w')  ##collinear gene pair
f4.write('#gene\tchr\tstart\tend\tgene\tchr\tstart\tend\tblock_ori\n')
for line in f3:
	if '## Alignment' in line and line.split(':')[0] in block:
		flag=1
		ori=line.split()[-1]
	elif '## Alignment' in line and line.split(':')[0] not in block:
		flag=0
	elif  '#' not in line[0] and flag:
		g1=line.split()[-3]; g2=line.split()[-2]
		f4.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n'.format(g1,gene[g1][0],gene[g1][1],gene[g1][2],g2,gene[g2][0],gene[g2][1],gene[g2][2],ori))
f4.close()
f3.close()
