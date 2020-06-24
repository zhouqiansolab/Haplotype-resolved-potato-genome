import sys
from itertools import islice

f1 = open(sys.argv[1]) ## RH_RH_best.gff
f2 = open(sys.argv[2]) ## .blast
f3 = open(sys.argv[3],'w')
f4 = open(sys.argv[4],'w')

spe = {}
for i in f1:
	i = i.strip().split()
	if i[0].startswith('ST4'):
		spe[i[1]] = 'ST'
		f4.write('{0}\tST|{1}\t{2}\t{3}\n'.format(i[0],i[1],i[2],i[3]))
	else:
		if i[0].startswith('chr'):
			if i[0][-1] == '1':
				f4.write('{0}\tHAP1|{1}\t{2}\t{3}\n'.format(i[0],i[1],i[2],i[3]))
				spe[i[1]] = 'HAP1'
			else:
				spe[i[1]] = 'HAP2'
				f4.write('{0}\tHAP2|{1}\t{2}\t{3}\n'.format(i[0],i[1],i[2],i[3]))
		else:
			spe[i[1]] = 'LG0'
			f4.write('{0}\tLG0|{1}\t{2}\t{3}\n'.format(i[0],i[1],i[2],i[3]))

for i in f2:
	i = i.strip().split()
	i[0] = spe[i[0]]+'|'+i[0]
	i[1] = spe[i[1]]+'|'+i[1]
	for a in i:
		f3.write('{0}\t'.format(a))
	f3.write('\n')

f1.close
f2.close
f3.close
