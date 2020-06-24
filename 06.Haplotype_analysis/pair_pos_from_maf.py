import sys

f1=open(sys.argv[1])  ## import maf file
f2=open(sys.argv[2],'w')   ##ourput paralog regions
f2.write('#hap1\tstart1\tend1\tori1\thap2\tstart2\tend2\tori2\n')
for line in f1:
	line=line.split()
	if len(line)==0:
		continue
	if line[0]== '#':
		info=''
	elif line[0]=="s" and info=='':
		info=line
	elif line[0]=="s" and info !='':
		if len(line) !=6 or len(info) !=6:
			print("ERROR",line)
			continue
		hap1=line[1].split('_')[0]+'_'+line[1].split('_')[1]
		ori1=line[4]
		if line[4] =="+":
			start1=int(line[1].split('_')[2])+int(line[2])
			end1=(start1+int(line[3]))
		else: #If the strand field is "-" then this is the start relative to the reverse-complemented source sequence.
			a=int(line[1].split('_')[2]); b=int(line[1].split('_')[3])
			end1= b-int(line[2])+1
			start1= b-int(line[2])-int(line[3])+1
		
		hap2=info[1].split('_')[0]+'_'+info[1].split('_')[1]
		ori2=info[4]
		if info[4]=="+":
			start2=int(info[1].split('_')[2])+int(info[2])
			end2=(start2+int(info[3]))
		else: #If the strand field is "-" then this is the start relative to the reverse-complemented source sequence.
			a=int(info[1].split('_')[2]); b=int(info[1].split('_')[3])
			end2= b-int(info[2])+1
			start2= b-int(info[2])-int(info[3])+1
		f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n'.format(hap1,start1,end1,ori1,hap2,start2,end2,ori2))
f1.close()
f2.close()
