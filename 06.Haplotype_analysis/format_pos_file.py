import sys

f1 = open(sys.argv[1])
f2 = open(sys.argv[2],'w')

flag,tmp = 0,{}
for i in f1:
	i = i.strip()
	if i.startswith('#'):
		flag = 1
		tmp[i] = []
	elif i.startswith('start'):
		if flag == 1:
			ID = tmp.keys()[0]
			f2.write('{0}\t{1}\n'.format(ID,i))
			for i in tmp[ID]:
				f2.write('{0}\n'.format(i))
			tmp,flag  = {},0
	else:
		ID = tmp.keys()[0]
		tmp[ID].append(i)

f1.close
f2.close
