

import os
import sys


f1=open(sys.argv[1])   ##input blasr output in m5 format
f2=open(sys.argv[2],'w')  ##output file

f2.write('#Que1\tQue2\tRef\tQ1_len\tQ2_len\tQ1_start\tQ1_end\tQ2_start\tQ2_end\tOri\tGap\n')

que=''
for line in f1:
	line=line.split()
	if line[0] !=que and que !='':
		for  i in range(1,flag-1):
			for j in range(i+1,flag):
				if int(map[i][3])-int(map[i][2])+int(map[j][3])-int(map[j][2])-(max(int(map[j][3]),int(map[i][3]))-min(int(map[i][2]),int(map[j][2]))) < 3000 and  int(map[i][3])-int(map[i][2])+int(map[j][3])-int(map[j][2])-(max(int(map[j][3]),int(map[i][3]))-min(int(map[i][2]),int(map[j][2]))) < min(int(map[i][6]),int(map[j][6]))/3:  ###the overlap(i,j) <3k and overlap(i,j)<0.3(min(len_i,len_j))
					if (map[i][5].split('_')[0]+'_'+map[i][5].split('_')[1] == map[j][5].split('_')[0]+'_'+map[j][5].split('_')[1]) or (map[i][5].split('_')[0] =="lg0" or map[j][5].split('_')[0] =="lg0"): ##i and j in same linkage group or belong to linkage group lg0.
						if map[i][9]+map[j][9]=='++' and int(map[i][6])-int(map[i][8]) <=2000 and int(map[j][7]) <=2000: # i_T -> j_H
							f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(map[i][5],map[j][5],que,map[i][6],map[j][6],int(map[i][7]),int(map[i][8]),int(map[j][7]),int(map[j][8]),'++',int(map[j][2])-int(map[i][3])))
							break
						if map[i][9]+map[j][9]=='+-' and int(map[i][6])-int(map[i][8]) <=2000 and int(map[j][6])-int(map[j][8]) <=2000: # i_T -> j_T
							f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(map[i][5],map[j][5],que,map[i][6],map[j][6],int(map[i][7]),int(map[i][8]),int(map[j][7]),int(map[j][8]),'+-',int(map[j][2])-int(map[i][3])))
							break
						if map[i][9]+map[j][9]=='-+' and int(map[i][7]) <=2000 and int(map[j][7]) <=2000: # i_H -> j_H
							f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(map[i][5],map[j][5],que,map[i][6],map[j][6],int(map[i][7]),int(map[i][8]),int(map[j][7]),int(map[j][8]),'-+',int(map[j][2])-int(map[i][3])))
							break
						if map[i][9]+map[j][9]=='--' and int(map[i][7]) <=2000 and int(map[j][6])-int(map[j][8]) <=2000: # i_H -> j_T
							f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(map[i][5],map[j][5],que,map[i][6],map[j][6],int(map[i][7]),int(map[i][8]),int(map[j][7]),int(map[j][8]),'--',int(map[j][2])-int(map[i][3])))
							break
	if line[0] !=que:
		que=line[0]
		map={};flag=1
	if que==line[0]:
		if flag==1:
			map[1]=line
		else:
			pre_aln=map[flag-1]
			if pre_aln[5].split('_')[0]+'_'+ pre_aln[5].split('_')[1] == line[5].split('_')[0]+'_'+ line[5].split('_')[1] and (int(line[3])-int(line[2])+int(pre_aln[3])-int(pre_aln[2]))-(max(int(line[3]),int(pre_aln[3]))-min(int(line[2]),int(pre_aln[2]))) > 0.75*(min(int(line[3])-int(line[2]),int(pre_aln[3])-int(pre_aln[2]))):  ##  the 'pre_aln' and the 'now_aln' may be coincident
				maplen={}; maplen[flag]=int(pre_aln[3])-int(pre_aln[2]); maplen[flag+1]=int(line[3])-int(line[2])
				iden={}; iden[flag]=int(pre_aln[11])/(int(pre_aln[11])+int(pre_aln[12])+int(pre_aln[13])); iden[flag+1]=int(line[11])/(int(line[11])+int(line[12])+int(line[13]))
				if iden[flag]>=0.99 and iden[flag] >iden[flag+1]:  ##save the pre_aln
					flag-=1
				elif iden[flag+1]>=0.99 and iden[flag+1] >iden[flag]:  ##save the now_aln
					flag-=1; map[flag]=line
				elif max(iden.values()) <0.99 and maplen[flag] > maplen[flag+1]: ##save the pre_aln
					flag-=1
				elif max(iden.values()) <0.99 and maplen[flag+1] > maplen[flag]: ##save the now_aln
					flag-=1; map[flag]=line
				else:
					map.pop(flag-1); flag-=2  ##the pre_aln and now_aln both are excluded
			else:
				map[flag]=line  ##save the now_aln
		flag+=1

for  i in range(1,flag-1):
	for j in range(i+1,flag):
		if int(map[i][3])-int(map[i][2])+int(map[j][3])-int(map[j][2])-(max(int(map[j][3]),int(map[i][3]))-min(int(map[i][2]),int(map[j][2]))) < 3000 and  int(map[i][3])-int(map[i][2])+int(map[j][3])-int(map[j][2])-(max(int(map[j][3]),int(map[i][3]))-min(int(map[i][2]),int(map[j][2]))) < min(int(map[i][6]),int(map[j][6]))/3:  ###the overlap(i,j) <3k and overlap(i,j)<0.3(min(len_i,len_j))
			if (map[i][5].split('_')[0]+'_'+map[i][5].split('_')[1] == map[j][5].split('_')[0]+'_'+map[j][5].split('_')[1]) or (map[i][5].split('_')[0] =="lg0" or map[j][5].split('_')[0] =="lg0"): ##i and j in same linkage group or belong to linkage group lg0.
				if map[i][9]+map[j][9]=='++' and int(map[i][6])-int(map[i][8]) <=2000 and int(map[j][7]) <=2000: # i_T -> j_H
					f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(map[i][5],map[j][5],que,map[i][6],map[j][6],int(map[i][7]),int(map[i][8]),int(map[j][7]),int(map[j][8]),'++',int(map[j][2])-int(map[i][3])))
					break
				if map[i][9]+map[j][9]=='+-' and int(map[i][6])-int(map[i][8]) <=2000 and int(map[j][6])-int(map[j][8]) <=2000: # i_T -> j_T
					f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(map[i][5],map[j][5],que,map[i][6],map[j][6],int(map[i][7]),int(map[i][8]),int(map[j][7]),int(map[j][8]),'+-',int(map[j][2])-int(map[i][3])))
					break
				if map[i][9]+map[j][9]=='-+' and int(map[i][7]) <=2000 and int(map[j][7]) <=2000: # i_H -> j_H
					f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(map[i][5],map[j][5],que,map[i][6],map[j][6],int(map[i][7]),int(map[i][8]),int(map[j][7]),int(map[j][8]),'-+',int(map[j][2])-int(map[i][3])))
					break
				if map[i][9]+map[j][9]=='--' and int(map[i][7]) <=2000 and int(map[j][6])-int(map[j][8]) <=2000: # i_H -> j_T
					f2.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'.format(map[i][5],map[j][5],que,map[i][6],map[j][6],int(map[i][7]),int(map[i][8]),int(map[j][7]),int(map[j][8]),'--',int(map[j][2])-int(map[i][3])))
					break
f1.close()
f2.close()
