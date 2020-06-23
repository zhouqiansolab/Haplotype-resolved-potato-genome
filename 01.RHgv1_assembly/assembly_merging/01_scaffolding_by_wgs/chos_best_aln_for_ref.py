

import os
import sys


##choose the best hit for every mapped interval on reference seq.

f1=open(sys.argv[1])  ##input blasr output file sorted by reference name and position
f2=open(sys.argv[2],'w')  ##output file

ref=''
for line in f1:
	line=line.split()
	if line[5] !=ref and ref !='':
		for i in range(1,flag):
			for j in map[i]:
				f2.write(j+'\t')
			f2.write('\n')
	if line[5] !=ref:
		ref=line[5];flag=1;map={}
	if ref==line[5]:
		if flag==1:
			map[flag]=line
		else:
			pre_aln=map[flag-1]
			if (int(line[8])-int(line[7])+int(pre_aln[8])-int(pre_aln[7]))-(max(int(line[8]),int(pre_aln[8]))-min(int(line[7]),int(pre_aln[7]))) > 0.5*(min(int(line[8])-int(line[7]),int(pre_aln[8])-int(pre_aln[7]))) or (int(line[8])-int(line[7])+int(pre_aln[8])-int(pre_aln[7]))-(max(int(line[8]),int(pre_aln[8]))-min(int(line[7]),int(pre_aln[7]))) > 5000:  ##  define the 'pre_aln' and the 'now_aln' are overlapped.
				maplen={}; maplen[flag]=int(pre_aln[3])-int(pre_aln[2]); maplen[flag+1]=int(line[3])-int(line[2])
				iden={}; iden[flag]=int(pre_aln[11])/(int(pre_aln[11])+int(pre_aln[12])+int(pre_aln[13])); iden[flag+1]=int(line[11])/(int(line[11])+int(line[12])+int(line[13]))
				if iden[flag]>=0.98 and iden[flag] >iden[flag+1]:  ##save the pre_aln
					flag-=1
				elif iden[flag+1]>=0.98 and iden[flag+1] >iden[flag]:  ##save the now_aln
					flag-=1; map[flag]=line
				elif max(iden.values()) <0.98 and maplen[flag] > maplen[flag+1]: ##save the pre_aln
					flag-=1
				elif max(iden.values()) <0.98 and maplen[flag+1] > maplen[flag]: ##save the now_aln
					flag-=1; map[flag]=line
				else:
					map.pop(flag-1); flag-=2  ##the pre_aln and now_aln both are excluded
			else:
				map[flag]=line  ##save the pre_aln and now_aln
		flag+=1

for i in range(1,flag):
	for j in map[i]:
		f2.write(j+'\t')
	f2.write('\n')
f1.close()
f2.close()
