import sys

f1=open(sys.argv[1])  ##input scaf len
f2=open(sys.argv[2])  ##input N-base bed file


scaf_len={}
for line in f1:
	line=line.split()
	scaf_len[line[0]]=int(line[1])
f1.close()

f3=open(sys.argv[3],'w')  ##output file
scaf=''
for line in f2:
	line=line.split()
	if scaf !=line[0] and scaf !='':
		f3.write('{0}_{1}\t{0}\t{2}\t{3}\n'.format(scaf,flag,start,scaf_len[scaf]))
		scaf_len.pop(scaf)
	if scaf !=line[0]:
		scaf=line[0]
		start=1
		flag=1
	if scaf==line[0]:
		f3.write('{0}_{1}\t{0}\t{2}\t{3}\n'.format(scaf,flag,start,int(line[1])-1))
		start= int(line[2])+1
		flag+=1
f2.close()

f3.write('{0}_{1}\t{0}\t{2}\t{3}\n'.format(scaf,flag,start,scaf_len[scaf]))
scaf_len.pop(scaf)

for scaf in scaf_len:
	f3.write('{0}_{1}\t{0}\t{2}\t{3}\n'.format(scaf,1,1,scaf_len[scaf]))

f3.close()
