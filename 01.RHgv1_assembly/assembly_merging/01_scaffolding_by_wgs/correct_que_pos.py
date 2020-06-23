

##because the query seq is splited into 50kb fragments before doing blasr, the query's position in alignment record should be transformed to the postion on the raw sequence of the query.

import sys
import os

f1=open(sys.argv[1])  ##input blasr output in m5 format
f2=open(sys.argv[2])  ##Input raw query length file
f3=open(sys.argv[3],'w')   ##output file

que_len={}
for line in f2:
	line=line.split()
	if '>' in line[0]:
		que_len[line[0][1:]]=int(line[-2])  ##circular may in query name
	else:
		que_len[line[0]]=int(line[-2])
f2.close()

for line in f1:
	line=line.split()
	start=int(line[0].split('_')[-1].split('-')[0])
	que_name=''
	for i in line[0].split('/')[0].split('_')[:-1]:
		que_name+=(i+'_')
	f3.write('{0}\t{1}\t{2}\t{3}'.format(que_name[:-1],que_len[que_name[:-1]],int(line[2])+start-1,int(line[3])+start-1))
	for j in line[4:]:
		f3.write('\t'+j)
	f3.write('\n')
f3.close()
f1.close()
