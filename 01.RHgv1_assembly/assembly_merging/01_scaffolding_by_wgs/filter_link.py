

import os
import sys

f1=open(sys.argv[1])  #Input file
f2=open(sys.argv[2],'w')  ##output txt file
f3=open(sys.argv[3],'w')  ##output dot file

f3.write('digraph 1 {\n')

info={}; link={}
for line in f1:
	if '#' in line:
		f2.write(line)
		continue
	lsp=line.split()
	if int(lsp[-1]) >30000 or int(lsp[-1]) < -2000:  ##-2k <= gap <=30k
		continue
	if int(lsp[2].split('_')[-1]) not in info:
		info[int(lsp[2].split('_')[-1])]=[]
	info[int(lsp[2].split('_')[-1])].append(line)
	if lsp[0] not in link:  ##only record in_orientation
		link[lsp[0]]={}; link[lsp[0]]['+']=[]; link[lsp[0]]['-']=[]
	if lsp[9][0]=='+':
		link[lsp[0]]['-'].append(lsp[1])  ##Link[A][-]=[B,C]
	else:
		link[lsp[0]]['+'].append(lsp[1])
	if lsp[1] not in link:  ##only record in_orientation
		link[lsp[1]]={}; link[lsp[1]]['+']=[]; link[lsp[1]]['-']=[]
	link[lsp[1]][lsp[9][1]].append(lsp[0])
f1.close()
rm_link=[]
for i in link:
	for j in link[i]:  ##for j in [+,-]:
		if len(link[i][j])>1:
			for s in link[i][j]:  ##for s in [B,C]
				rm_link.append([i,s])  ##rm_link[A,C]
link.clear()

color={}; color['++']='blue'; color['--']='green'; color['+-']='orange'; color['-+']='red'
rev_ori={}; rev_ori['++']='--'; rev_ori['+-']='+-'; rev_ori['-+']='-+'; rev_ori['--']='++'
info_srt=list(info.keys()); info_srt.sort()
for i in info_srt:
	for s in info[i]:
		j=s.split()
		if [j[0],j[1]] not in rm_link and [j[1],j[0]] not in rm_link:
			f2.write(s)
			line=s.split()
			f3.write('"{0}" -> "{1}" [label="{2}:{3}:{4}" color="{5}"]\n'.format(line[0]+'_'+line[3]+'bp',line[1]+'_'+line[4]+'bp',line[9],line[10],line[2],color[line[9]]))
			f3.write('"{0}" -> "{1}" [label="{2}:{3}:{4}" color="{5}"]\n'.format(line[1]+'_'+line[4]+'bp',line[0]+'_'+line[3]+'bp',rev_ori[line[9]],line[10],line[2],color[rev_ori[line[9]]]))
			#f3.write('"{0}" -> "{1}" [label="{2}" color="{3}"]\n'.format(line[1]+'_'+line[4]+'bp',line[0]+'_'+line[3]+'bp',rev_ori[line[9]],color[rev_ori[line[9]]]))
f3.write('}\n')
f2.close()
f3.close()
