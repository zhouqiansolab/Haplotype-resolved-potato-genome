

import sys

f1=open(sys.argv[1])  ##input window information  ###remove duplicated scaffold ids.
f2=open(sys.argv[2],'w')   ##output normalized reads number within a window.
mq=int(sys.argv[3])    ##MQ threshold

f2.write('#window\treal_reads\tratio\tnorm_reads\n')

ctg_win={}; win_srt=[]
for  line in f1:
	if '#' in line:
		continue
	lsp=line.split()
	win_srt.append(lsp[0]+'-'+lsp[1]+'-'+lsp[-2])   ###win_srt=[Win12-Scaf4-400001,Win13-Scaf5-1]
	if lsp[1] not in ctg_win:
		ctg_win[lsp[1]]={}
	ctg_win[lsp[1]][int(lsp[-2])]=0  ##ct_win[Scaf16_lg0][1]=0
f1.close()

total=0
for line in sys.stdin:  ##read in the sam lines from *.bam
	line=line.split()
	if line[5]=='*':
		continue
	if 'H' in line[5] or 'S' in line[5]  or ('NM:i:' in line[11] and int(line[11][5:]) >3) :
		continue
	if int(line[4]) <mq:   ##can add other criteria
		continue
	total+=1; ctg=line[2]
	if ctg not in ctg_win:
		continue
	
	###
	a=(int(line[3])//100000)*100000+1   ## ##find the right window  ##100000 presents the window size
	if a not in ctg_win[ctg]:
		print(line[2],line[3],'ERROR')
	ctg_win[ctg][a]+=1
	####

for w in win_srt:
	win_num=ctg_win[w.split('-')[1]][int(w.split('-')[2])]
	f2.write('{0}\t{1}\t{2}\t{3}\n'.format(w.split('-')[0],win_num,round(win_num/total,10),int(win_num/total*10000000)))
f2.close()
