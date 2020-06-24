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
flag=1
for i in f2:
	if '#' ==i[0]:
		continue
	i = i.strip().split()
	filename1 = '02_diff/'+str(flag)+'_'+i[0] + '.fa'
	filename2 = '02_diff/'+str(flag)+'_'+i[4] + '.fa'
	f3 = open(filename1,'w')
	f4 = open(filename2,'w')
	f3.write('>{0}_{1}_{2}_{3}bp\n{4}'.format(i[0],i[1],i[2],int(i[2])-int(i[1]),FASTA[i[0]][int(i[1]):int(i[2])]))  ##caution;trap here
	f4.write('>{0}_{1}_{2}_{3}bp\n{4}'.format(i[4],i[5],i[6],int(i[6])-int(i[5]),FASTA[i[4]][int(i[5]):int(i[6])]))  ##caution;trap here
	flag+=1
	f3.close
	f4.close

f1.close
f2.close
