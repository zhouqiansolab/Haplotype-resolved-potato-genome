import sys
import os

f1 = open(sys.argv[1])
f2 = open('lastz.2.sh','w')

flag=1
for i in f1:
	if '#' in i[0]:
		continue
	i = i.strip().split()
	ID= '06_diff/'+str(flag)+'_'+i[0].split('_')[0]
	if i[3] == '+' and i[7] =='+':
		cmd = 'lastz '+ID+'_2.fa '+ID+'_1.fa --chain  --format=differences  --matchcount=3000 --strand=plus --ambiguous=n|cut -f 1-12 > '+ID+'.diff'
	else:
		cmd = 'lastz '+ID+'_2.fa '+ID+'_1.fa --chain  --format=differences  --matchcount=3000 --strand=minus --ambiguous=n|cut -f 1-12 > '+ID+'.diff'
	f2.write('{0}\n'.format(cmd))
	flag+=1
f1.close
f2.close()
