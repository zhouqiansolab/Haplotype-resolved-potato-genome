#!/public/agis/huangsanwen_group/zhouqian/bin/python3.2

f1=open('10x_wgs.aln')
f2=open('10x_wgs.aln2','w')

for line in f1:
	line=line.split()
	f2.write(line[0].split('/')[0])
	for i in line[1:]:
		f2.write('\t'+i)
	f2.write('\n')
f1.close()
f2.close()
