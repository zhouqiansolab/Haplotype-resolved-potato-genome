import sys
from itertools import islice

f1 = open(sys.argv[1]) ## gff
f2 = open(sys.argv[2]) ## collinearity
f3 = open(sys.argv[3],'w')

gff = {}
for i in f1:
	i = i.strip().split()
	gff[i[1]] = [i[0],i[2]]

start1,end1,start2,end2,flag = [0,0],[0,0],[0,0],[0,0],1
#for i in islice(f2, 11, None):
for i in f2:
	if i.startswith('## Alignment'):
		f3.write('start1: {0}\t{1}\tend1: {2}\t{3}\tlength1: {4}\t'.format(start1[0],start1[1],end1[0],end1[1],abs(int(end1[1]) - int(start1[1]))))
		f3.write('start2: {0}\t{1}\tend2: {2}\t{3}\tlength2: {4}\n'.format(start2[0],start2[1],end2[0],end2[1],abs(int(end2[1]) - int(start2[1]))))
		f3.write('{0}'.format(i))
		flag = 1
	else:
		if '#' in i[0]:
			continue
		i = i.strip()
		a = i.split()
		if flag == 1:
			start1 = gff[a[-3]]
			start2 = gff[a[-2]]
			flag = 0
		end1 = gff[a[-3]]
		end2 = gff[a[-2]]
		f3.write('{0}\t{1}\t{2}\n'.format(i,gff[a[-3]],gff[a[-2]]))
f3.write('start1: {0}\t{1}\tend1: {2}\t{3}\tlength1: {4}\t'.format(start1[0],start1[1],end1[0],end1[1],abs(int(end1[1]) - int(start1[1]))))
f3.write('start2: {0}\t{1}\tend2: {2}\t{3}\tlength2: {4}\n'.format(start2[0],start2[1],end2[0],end2[1],abs(int(end2[1]) - int(start2[1]))))

f1.close
f2.close
f3.close
