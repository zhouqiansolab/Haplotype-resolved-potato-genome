#!/public/agis/huangsanwen_group/zhouqian/bin/python3.2

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
		if len(newseq) <= 80000:  ##If seq <=80kb, do not split it.
			f2.write('{0}_{1}-{2}\t{2}\n{3}\n'.format(name,1,len(newseq),newseq))
		else:
			for i in range(0,len(newseq)//50000):
				f2.write('{0}_{1}-{2}\t50000\n{3}\n'.format(name,i*50000+1,(i+1)*50000,newseq[i*50000:(i+1)*50000]))
			f2.write('{0}_{1}-{2}\t{3}\n{4}\n'.format(name,(i+1)*50000+1,len(newseq),len(newseq)-(i+1)*50000,newseq[(i+1)*50000:-1]))
		name=line.split()[0]
		newseq=''
	elif '>' not in line:
		newseq+=line.strip()
		
f2.close()
f1.close()
