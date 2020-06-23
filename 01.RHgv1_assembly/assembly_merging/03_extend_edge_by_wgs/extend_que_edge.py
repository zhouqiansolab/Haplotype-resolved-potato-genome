

### the overhang of reference can be used to extend the edge of the query


import os
import sys

f1=open(sys.argv[1])  ##input blasr output in m5 format sorted by reference position
f2=open(sys.argv[2],'w')  ##output file

f2.write('#que\tref\tadd_pos\tref_start\tref_end\tori\n')
ref=''
for line in f1:
	line=line.split()
	iden_ref=int(line[11])/(int(line[11])+int(line[12])+int(line[14]))
	iden_que=int(line[11])/(int(line[11])+int(line[12])+int(line[13]))
	cov_que=(int(line[3])-int(line[2]))/int(line[1])
	###filter the map   saving the mapping: map>5k iden>98%; >3k iden>99; else iden >99.5 %
	if (int(line[3])-int(line[2]) <3000 and iden_que < 0.995) or (3000 <= int(line[3])-int(line[2]) <5000 and iden_que <0.99 ) or (int(line[3])-int(line[2])>=5000 and iden_que<0.98):
		continue
	
	if line[5] !=ref and ref!='':
		if int(map_1[2]) <500 and (map_1[9]=='+' and int(map_1[7])>800) :  ##ref overhangs >800bp at head  ##extend the head of que
			f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(map_1[0],map_1[5],'H',1,int(map_1[7])-1,'+'))
		elif int(map_1[1])-int(map_1[3]) <500 and map_1[9]=='-' and int(map_1[7])>800 : ##ref overhangs >800bp at head  ##extend the tail of que
			f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(map_1[0],map_1[5],'T',1,int(map_1[7])+1,'-'))
		
		if int(map_2[1])-int(map_2[3]) <500 and (map_2[9]=='+' and int(map_2[6])- int(map_2[8])>800) :  ##ref overhangs >800bp at tail  ##extend the tail of que
			f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(map_2[0],map_2[5],'T',int(map_2[8])+1,int(map_2[6]),'+'))
		elif int(map_2[2]) <500 and map_2[9]=='-' and  int(map_2[6])- int(map_2[8]) >800: ##ref overhangs >800bp at tail  ##extend the head of que
			f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(map_2[0],map_2[5],'H',int(map_2[8])+1,int(map_2[6]),'-'))

	if line[5] !=ref:
		ref=line[5]
		map_1=line
	if ref ==line[5]:
		map_2=line

if int(map_1[2]) <500 and (map_1[9]=='+' and int(map_1[7])>800) :  ##ref overhangs >800bp at head  ##extend the head of que
	f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(map_1[0],map_1[5],'H',1,int(map_1[7])-1,'+'))
elif int(map_1[1])-int(map_1[3]) <500 and map_1[9]=='-' and int(map_1[7])>800 : ##ref overhangs >800bp at head  ##extend the tail of que
	f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(map_1[0],map_1[5],'T',1,int(map_1[7])+1,'-'))

if int(map_2[1])-int(map_2[3]) <500 and (map_2[9]=='+' and int(map_2[6])- int(map_2[8])>800) :  ##ref overhangs >800bp at tail  ##extend the tail of que
	f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(map_2[0],map_2[5],'T',int(map_2[8])+1,int(map_2[6]),'+'))
elif int(map_2[2]) <500 and map_2[9]=='-' and  int(map_2[6])- int(map_2[8]) >800: ##ref overhangs >800bp at tail  ##extend the head of que
	f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(map_2[0],map_2[5],'H',int(map_2[8])+1,int(map_2[6]),'-'))


f1.close()
f2.close()
