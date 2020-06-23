

##if two queries with consecutive ids are covered by same reference seq, then the reference seq can fill the gap between the two queries.

import os
import sys

f1=open(sys.argv[1])  ##input blasr output file sorted by reference seq
f2=open(sys.argv[2],'w')  ##output link.txt file  ##consecutive contigs   are linked with  proper orientation
f3=open(sys.argv[3],'w')  ##output link.txt file  ##consecutive contigs are linked  in inappropriate orientation

f2.write('#Que1\tQue2\tRef\tOri\tGap_start_ref\tGap_end_ref\tQ1_len\tQ2_len\tQ1_start\tQ1_end\tQ2_start\tQ2_end\n')
ref=''
for line in f1:
	line=line.split()
	if line[5] !=ref and ref !='':
		for i in range(1,flag-1):
			map_i=map[i]
			name_i_1='';name_i_2=int(map_i[0].split('/')[0].split('_')[-1])  ##que='lg1_2_3727_2' ; name_i_1='lg1_2_3727'  name_i_2='2'
			for tmp in map_i[0].split('/')[0].split('_')[:-1]:
				name_i_1+=(tmp+'_')
			name_i_1=name_i_1[:-1]
			
			for j in range(i+1,flag):
				map_j=map[j]
				name_j_1='';que_j_2=int(map_j[0].split('/')[0].split('_')[-1])  ##que='lg1_2_3727_3' ; name_j_1='lg1_2_3727'  name_j_2='3'
				for tmp in map_j[0].split('/')[0].split('_')[:-1]:
					name_j_1+=(tmp+'_')
				name_j_1=name_j_1[:-1]
				
				if ( name_i_1 == name_j_1 and name_i_2-que_j_2 ==1 and map[i][9]+map[j][9]=='--') or (name_i_1 == name_j_1 and name_i_2-que_j_2 ==-1 and map[i][9]+map[j][9]=='++') : ##check if i and j are consecutive contigs  and are linked with  proper orientation
					if int(map[j][7])-int(map[i][8]) >=0 or (int(map[j][7])-int(map[i][8]) <0 and int(map[i][8])-int(map[j][7]) < min(int(map[i][8])-int(map[i][7]), int(map[j][8])-int(map[j][7]))/3) : ##the gap between i and j should be >0 or the overlap should be < 1/3* min(map_len_i,map_len_j)
						f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n'.format(map[i][0].split('/')[0],map[j][0].split('/')[0],ref,map[i][9]+map[j][9],map[i][8],map[j][7],map[i][1],map[j][1],map[i][2],map[i][3],map[j][2],map[j][3]))
						break
				elif name_i_1 == name_j_1 and abs(name_i_2-que_j_2)==1 :  ##  i and j are consecutive contigs but in inappropriate orientation
					if int(map[j][7])-int(map[i][8]) >=0 or (int(map[j][7])-int(map[i][8]) <0 and int(map[i][8])-int(map[j][7]) < min(int(map[i][8])-int(map[i][7]), int(map[j][8])-int(map[j][7]))/3) : ##the gap between i and j should be >0 or the overlap should be < 1/3* min(map_len_i,map_len_j)
						f3.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n'.format(map[i][0].split('/')[0],map[j][0].split('/')[0],ref,map[i][9]+map[j][9],map[i][8],map[j][7],map[i][1],map[j][1],map[i][2],map[i][3],map[j][2],map[j][3]))
						break

	if line[5] !=ref:
		ref=line[5];map={}; flag=1
	if ref==line[5]:
		map[flag]=line
		flag+=1


for i in range(1,flag-1):  ##for the last ref
	map_i=map[i]
	name_i_1='';name_i_2=int(map_i[0].split('/')[0].split('_')[-1])  ##que='lg1_2_3727_2' ; name_i_1='lg1_2_3727'  name_i_2='2'
	for tmp in map_i[0].split('_')[:-1]:
		name_i_1+=(tmp+'_')
	name_i_1=name_i_1[:-1]
	
	for j in range(i+1,flag):
		map_j=map[j]
		name_j_1='';que_j_2=int(map_j[0].split('/')[0].split('_')[-1])  ##que='lg1_2_3727_3' ; name_j_1='lg1_2_3727'  name_j_2='3'
		for tmp in map_j[0].split('_')[:-1]:
			name_j_1+=(tmp+'_')
		name_j_1=name_j_1[:-1]

		if ( name_i_1 == name_j_1 and name_i_2-que_j_2 ==1 and map[i][9]+map[j][9]=='--') or (name_i_1 == name_j_1 and name_i_2-que_j_2 ==-1 and map[i][9]+map[j][9]=='++') : ##check if i and j are consecutive contigs  and are linked with  proper orientation
			if int(map[j][7])-int(map[i][8]) >=0 or (int(map[j][7])-int(map[i][8]) <0 and int(map[i][8])-int(map[j][7]) < min(int(map[i][8])-int(map[i][7]), int(map[j][8])-int(map[j][7]))/3) : ##the gap between i and j should be >0 or the overlap should be < 1/3* min(map_len_i,map_len_j)
				f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n'.format(map[i][0].split('/')[0],map[j][0].split('/')[0],ref,map[i][9]+map[j][9],map[i][8],map[j][7],map[i][1],map[j][1],map[i][2],map[i][3],map[j][2],map[j][3]))
				break
		elif name_i_1 == name_j_1 and abs(name_i_2-que_j_2)==1 :  ##  i and j are consecutive contigs but in inappropriate orientation
			if int(map[j][7])-int(map[i][8]) >=0 or (int(map[j][7])-int(map[i][8]) <0 and int(map[i][8])-int(map[j][7]) < min(int(map[i][8])-int(map[i][7]), int(map[j][8])-int(map[j][7]))/3) : ##the gap between i and j should be >0 or the overlap should be < 1/3* min(map_len_i,map_len_j)
				f3.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n'.format(map[i][0].split('/')[0],map[j][0].split('/')[0],ref,map[i][9]+map[j][9],map[i][8],map[j][7],map[i][1],map[j][1],map[i][2],map[i][3],map[j][2],map[j][3]))
				break

		

f1.close()
f2.close()
