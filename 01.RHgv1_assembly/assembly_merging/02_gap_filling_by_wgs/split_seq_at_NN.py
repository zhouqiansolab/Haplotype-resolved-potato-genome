

import re
import sys
import os

f1=open(sys.argv[1])  ### input raw contigs
f2=open(sys.argv[2],'w') ### output splited contigs

name=''
for line in f1:
	if '>' in line and name =='':
		name=line.split()[0]
		newseq=''
	elif '>' in line and name!=line.split()[0]:
		flag=1
		for i in newseq.split('N'):
			if len(i)>0:
				f2.write('{0}_{1} splited from scaffold\n{2}\n'.format(name,flag,i))
				flag+=1
		name=line.split()[0]
		newseq=''
	elif '>' not in line:
		newseq+=line.strip()
flag=1
for i in newseq.split('N'):
	if len(i)>0:
		f2.write('{0}_{1}\n{2}\n'.format(name,flag,i))
		flag+=1
f1.close()
f2.close()
