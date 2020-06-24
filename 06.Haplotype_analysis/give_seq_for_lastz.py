import sys

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

def fasta(file):
	dic, k, v = {}, '', []
	for i in file:
		i = i.strip()
		if i.startswith('>'):
			dic[k] = "".join(v)
			k = i.split()[0][1:]
			v = []
		else:
			v.append(i)
	dic[k] = "".join(v)
	dic.pop('')
	return dic

FASTA = fasta(f1)

for i in f2:
	i = i.strip().split()
	filename1 = i[1][:-1] + '_' +i[3][-1] + '.fa'
	filename2 = i[1][:-1] + '_' +i[7][-1] + '.fa'
	f3 = open(filename1,'w')
	f4 = open(filename2,'w')
	f3.write('>{0}_{1}_{2}_{3}bp\n{4}'.format(i[3],i[4],i[5],i[6],FASTA[i[3]][int(i[4]):int(i[5])]))  ##caution;trap here
	if int(i[8]) < int(i[9]):
		f4.write('>{0}_{1}_{2}_{3}bp\n{4}'.format(i[7],i[8],i[9],i[10],FASTA[i[7]][int(i[8]):int(i[9])]))  ##caution;trap here
	else:
		f4.write('>{0}_{1}_{2}_{3}bp\n{4}'.format(i[7],i[9],i[8],i[10],FASTA[i[7]][int(i[9]):int(i[8])]))  #caution;trap here
	f3.close
	f4.close

f1.close
f2.close
