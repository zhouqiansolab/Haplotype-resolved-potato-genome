from __future__ import division 
import sys

f1 = open(sys.argv[1])
f2 = open(sys.argv[2],'w')
f3 = open(sys.argv[3],'w')

CHR = ''
for i in f1:
	a = i.strip().split()
	chr1 = a[9].split('_')
	chr2 = a[17].split('_')
	if 'chr' in a[9] and 'chr' in a[17]:
		if (a[9]=="chr0" and a[17]=="chr0") or (chr1[0] == chr2[0] and chr1[1] != chr2[1]):
			if 1/4 < int(a[15]) / int(a[23]) < 4 :
				print i.strip()
				if a[9] != CHR:  ## ## calculate for every chr
					if CHR != '':
						for e in stock:
							f2.write('{0}\t'.format(e))
						f2.write('\n')
					CHR,stock = a[9],a
				else:
					if int(a[10]) < int(stock[13]):
						if int(a[13]) < int(stock[13]): ## contained
							continue
						else:
							if (int(stock[13]) - int(a[10]))/min(int(stock[15]),int(a[15])) > 0.5:  ### overlap more than elongate
								if int(stock[15]) > int(a[15]):
									continue
								else:
									stock = a
							else:
								for e in stock:
									f2.write('{0}\t'.format(e))
								f2.write('\n')
								stock = a
					else:
						for e in stock:
							f2.write('{0}\t'.format(e))
						f2.write('\n')
						stock = a
		else:
			f3.write('{0}'.format(i))

f1.close
f2.close
