import re
import sys
import os

f1=open(sys.argv[1])  ### input raw contigs
f2=open(sys.argv[2],'w') ### output splited contigs
max_len=int(sys.argv[3])

name=''
for line in f1:
	if '>' in line and name =='':
		name=line.split()[0]
		newseq=''
	elif '>' in line and name!=line.split()[0]:
		if len(newseq) <= max_len:  ##If seq <=max_len, do not split it.
			f2.write('{0}_{1}-{2}\t{2}\n{3}\n'.format(name,1,len(newseq),newseq))
		else:
			for i in range(0,len(newseq)//max_len):
				f2.write('{0}_{1}-{2}\t{3}\n{4}\n'.format(name,i*max_len+1,(i+1)*max_len,max_len,newseq[i*max_len:(i+1)*max_len]))
			f2.write('{0}_{1}-{2}\t{3}\n{4}\n'.format(name,(i+1)*max_len+1,len(newseq),len(newseq)-(i+1)*max_len,newseq[(i+1)*max_len:-1]))
		name=line.split()[0]
		newseq=''
	elif '>' not in line:
		newseq+=line.strip()
		
if len(newseq) <= max_len:  ##If seq <=max_len, do not split it.
	f2.write('{0}_{1}-{2}\t{2}\n{3}\n'.format(name,1,len(newseq),newseq))
else:
	for i in range(0,len(newseq)//max_len):
		f2.write('{0}_{1}-{2}\t{3}\n{4}\n'.format(name,i*max_len+1,(i+1)*max_len,max_len,newseq[i*max_len:(i+1)*max_len]))
	f2.write('{0}_{1}-{2}\t{3}\n{4}\n'.format(name,(i+1)*max_len+1,len(newseq),len(newseq)-(i+1)*max_len,newseq[(i+1)*max_len:-1]))
f2.close()
f1.close()
