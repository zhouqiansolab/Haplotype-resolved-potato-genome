import sys
import os

path = sys.argv[1] # directory
files= os.listdir(path) # list all files under the directory
s = []
SNP, INDEL, INDEL_ALL = 0, [0] * 51, 0
for file in files:
	if '.diff' not in file:
		continue
	if not os.path.isdir(file): # open the file if it's not a directory
		f = open(path+"/"+file)
		for i in f: # read the file
			i = i.strip().split()
			if '-' not in i[10] and '-' not in i[11]:
				SNP += len(i[10])
			else:
				INDEL_ALL += 1
				if len(i[10]) < 50:
					INDEL[len(i[10])] += 1
				else:
					INDEL[50] += 1
		f.close

output = open(sys.argv[2],'w')
output.write('SNP\t1\t{0}\nINDEL\tall\t{1}\n'.format(SNP,INDEL_ALL))
for a in range(1,51):
	output.write('INDEL\t{0}\t{1}\n'.format(a,INDEL[a]))
output.close
