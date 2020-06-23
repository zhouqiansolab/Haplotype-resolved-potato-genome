
import os
import re
import sys


######this version  can solve the situation that in_num > 2 but not out_num >2; for cut_tip: if the path for the current node is the shorest one, cut the path.  if not, just leave the node , find a new node and go on walking; but if len(tip)==2, the shorter one must be cut and the longer one should be saved.

os.system('date')

linkf=open(sys.argv[1])  ##input link dot file
newconfa=open(sys.argv[2],'w')  ##output  flatted contig links as new contig fasta file


rever_ori={}
rever_ori['+']='-'
rever_ori['-']='+'

in_info={}
in_info['+']={}
in_info['-']={}
out_info={}
out_info['+']={}
out_info['-']={}

#single_ctg=[]
dot_pair={}
for line in linkf:
	if '{' in line or '}' in line:
		continue
	if '->' not in line:
#		single_ctg.append(line.strip())
		continue
	line=line.split(' ',3)
	if line[0] not in in_info['+']:
		in_info['+'][line[0]]=[]
		in_info['-'][line[0]]=[]
		out_info['+'][line[0]]=[]
		out_info['-'][line[0]]=[]
	if line[2] not in in_info['+']:
		in_info['+'][line[2]]=[]
		in_info['-'][line[2]]=[]
		out_info['+'][line[2]]=[]
		out_info['-'][line[2]]=[]
	out_info[line[3].split('"')[1].split(':')[0][0]][line[0]].append([line[2],line[3].split('"')[1].split(':')[1],line[3].split('"')[1].split(':')[0][1]])
	in_info[line[3].split('"')[1].split(':')[0][1]][line[2]].append([line[0],line[3].split('"')[1].split(':')[1],line[3].split('"')[1].split(':')[0][0]])   ###info_['+'][a]=[b,12345,'+']
	dot_pair[line[0]+'/'+line[2]]=0
linkf.close()

virtual_dotpair={}  ####if  A<->B , C->B, D->B, when remove A ,but don't known where the  <-B  should be moved to. so introduct a dictionary "virtual_dotpair".

node_list1=[]
node_list2=[]
node_list3=[]
for nodepair in dot_pair:
	node=nodepair.split('/')[0]
	if len(out_info['+'][node])==1 and len(out_info['-'][node])==1 and len(in_info['+'][node])==1 and len(in_info['-'][node])==1:
		node_list1.append(node)  ### inside and well-organized node
	elif  len(out_info['+'][node]) + len(out_info['-'][node])==1  and len(in_info['+'][node]) + len(in_info['-'][node])==1 and nodepair.split('/')[1]+'/'+nodepair.split('/')[0] in dot_pair:
		node_list2.append(node)  ### terminal node
	else:
		node_list3.append(node)  ###troubled node
node_list=(node_list1+node_list2+node_list3)
node_list1=[]
node_list2=[]
node_list3=[]

for nodepair in dot_pair:
	if nodepair.split('/')[1]+'/'+nodepair.split('/')[0] not in dot_pair:  #####make  up  the dot link to make all the links are two-headed.
		for i in out_info['+'][nodepair.split('/')[0]]:
			if i[0]==nodepair.split('/')[1]:
				in_info['-'][nodepair.split('/')[0]].append([i[0],i[1],rever_ori[i[2]]])
		for i in out_info['-'][nodepair.split('/')[0]]:
			if i[0]==nodepair.split('/')[1]:
				in_info['+'][nodepair.split('/')[0]].append([i[0],i[1],rever_ori[i[2]]])
		for i in in_info['+'][nodepair.split('/')[1]]:
			if i[0]==nodepair.split('/')[0]:
				out_info['-'][nodepair.split('/')[1]].append([i[0],i[1],rever_ori[i[2]]])
		for i in in_info['-'][nodepair.split('/')[1]]:
			if i[0]==nodepair.split('/')[0]:
				out_info['+'][nodepair.split('/')[1]].append([i[0],i[1],rever_ori[i[2]]])

def walk_node(node,in_info,out_info,orient,used_node,step,flag):
	path=[]
	overlap=0
	out_num=len(out_info[orient][node])
	#in_num=len(in_info[orient][node])
	in_num=1   ###in_num >1 means the initial node in_num>1; but if the  out_num==1, the path is valid.
	while (in_num<=1 or flag):          #### only when the node is the  terminal node the in_num=0  ###if flag==0, only in_num<=1 works; if flag==1, it allows in_num>1 when walking.
		path.append([node,orient,overlap])
		used_node[node+orient]=0
		if len(path)>=step:
			break
		if out_num !=1:
			break
		in_num=len(in_info[out_info[orient][node][0][2]][out_info[orient][node][0][0]])  #########out_info[orient][node][0][0] is the next node; out_info[orient][node][0][2] is the oritent of the next node
		out_num=len(out_info[out_info[orient][node][0][2]][out_info[orient][node][0][0]])  #########out_info[orient][node][0][0] is the next node; out_info[orient][node][0][2] is the oritent of the next node
		overlap=out_info[orient][node][0][1]
		new_node=out_info[orient][node][0][0]
		orient=out_info[orient][node][0][2]
		node=new_node
		if flag==0 and node+orient in used_node:  ####solve the circle when get_path; edited at  1/Dec/2015
			break
	return(node,orient,path,used_node)

def rm_link(a,b,orient,out_info,in_info):   ## the orient is for a output
	orient_a=orient
	for m in out_info[orient][a]:
		if b ==m[0]:
			orient_b=m[2]
			out_info[orient_a][a].remove(m)
	for m in in_info[orient_b][b]:
		if a ==m[0]:
			in_info[orient_b][b].remove(m)
	for m in in_info[rever_ori[orient]][a]:
		if b ==m[0]:
			orient_b=m[2]
			in_info[rever_ori[orient]][a].remove(m)
	for m in out_info[orient_b][b]:
		if a ==m[0]:
			out_info[orient_b][b].remove(m)
	print('ok1',a,b)
	return(out_info,in_info)

def rm_dotpair(a,b,dot_pair):
	if a+'/'+b in dot_pair:
		dot_pair.pop(a+'/'+b)
	if b+'/'+a in dot_pair:
		dot_pair.pop(b+'/'+a)
	print('ok2',a,b)
	return(dot_pair)
def add_dotpair(a,b,dot_pair):
	dot_pair[a+'/'+b]=0   ### only add output. can not add input.
	#dot_pair[b+'/'+a]=0
	print('ok3',a,b)
	return(dot_pair)

def cal_path_length(path):
	sum1=0
	sum2=0
	for i in path:
		sum1+=(int(i[0].split('bp')[0].split('_')[-1]))
		sum2+=(int(i[2]))
	path_len=(sum1-sum2)
	return(path_len)

def cut_tip(A,B,orient,out_info,in_info,used_tmp,dot_pair,virtual_dotpair):
	cut=0
	print(A,'cut_tip') ### the 'orient' is for B input.
	nodes={}
	for n in in_info[orient][B]:
		nodes[n[0]]=n[2]  ### the orient is for 'a' output in the link 'a->b'.
	paths={}
	paths_len={}
	for n in nodes:
		(node,orient2,paths[n],used_node1)=walk_node(n,in_info,out_info,rever_ori[nodes[n]],used_tmp,10,1) ###allow in_num>1 when walking to find out the potential path
		paths_len[n]=cal_path_length(paths[n])
		print(n,paths_len[n],paths[n])
	if len(paths[A])==1 and A+'/'+B in dot_pair and B+'/'+A not in dot_pair:
		dot_pair=rm_dotpair(A,B,dot_pair)
		(out_info,in_info)=rm_link(A,B,nodes[A],out_info,in_info)
		cut=1
	else:
		node_list=list(paths.keys())
		length_list=list(paths_len.values())
		bubble=0
		for i in range(0,len(node_list)-1):
			for j in range(i+1,len(node_list)):
				for i_path in paths[node_list[i]]:
					for j_path in paths[node_list[j]]:
						if i_path[0]==j_path[0]:    ### two paths generate a  bubble structure.
							bubble=1
							break
					if bubble :
						break
				if bubble:
					break
			if bubble:
				break     ###if bubble, cut=0
		if bubble!=1 and  len(paths_len)==2 and length_list[0]!=length_list[1] and  min(length_list) <=100000:   ####There are only two nodes at this site. ##the tips should be <100k
			for n in paths_len:
				if paths_len[n] == min(length_list) :
					bad_node=n
				else:
					good_node=n
			if B+'/'+bad_node in dot_pair:
				dot_pair=add_dotpair(B,good_node,dot_pair) #### remove other link between other nodes and B and complete the link A<->B
			elif B+'/'+bad_node in virtual_dotpair  and B+'/'+good_node in virtual_dotpair:
				dot_pair=add_dotpair(B,good_node,dot_pair) #### remove other link between other nodes and B and complete the link A<->B
				virtual_dotpair.pop(B+'/'+bad_node)
				virtual_dotpair.pop(B+'/'+good_node)
			dot_pair=rm_dotpair(bad_node,B,dot_pair)
			(out_info,in_info)=rm_link(bad_node,B,nodes[bad_node],out_info,in_info)
			cut=1
		elif bubble !=1 and len(paths_len)>2 and paths_len[A] == min(length_list) and paths_len[A] <=100000:    ####only remove the link A->B when the path of A is the shorest one. don't change other links
			if B+'/'+A in dot_pair:
				for n in nodes:
					if n !=A:
						virtual_dotpair[B+'/'+n]=0
			dot_pair=rm_dotpair(A,B,dot_pair)
			(out_info,in_info)=rm_link(A,B,nodes[A],out_info,in_info)  ####if  A<->B , C->B, D->B, when remove A ,but don't known where the  <-B  should be moved to. so introduct a dictionary virtual_dotpair.
			cut=1
	return(out_info,in_info,dot_pair,virtual_dotpair,cut)

def cut_bubble(node,orient,in_info,out_info,used_tmp,dot_pair):
	print(node,'cut_bubble')
	(node1,orient1,path1,used_node1)=walk_node(out_info[orient][node][0][0],in_info,out_info,out_info[orient][node][0][2],used_tmp,5,1)  ###allow in_num>1 when walking to find out the potential path
	(node2,orient2,path2,used_node2)=walk_node(out_info[orient][node][1][0],in_info,out_info,out_info[orient][node][1][2],used_tmp,5,1)  ###allow in_num>1
	print(node1,path1)
	print(node2,path2)
	cut=0
	for i in path1:
		for j in path2:
			if i[0] ==j[0]:  ###path1 and path2 meet at one node. There is a bubble here.
				if (path1.index(i)  < path2.index(j)) or (path1.index(i) == path2.index(j) and cal_path_length(path1) < cal_path_length(path2)) : ###path2 includes more nodes than path1  ## two paths include same node.  so comapre the lengths of two paths.
					dot_pair=rm_dotpair(node,out_info[orient][node][0][0],dot_pair)
					dot_pair=add_dotpair(node,out_info[orient][node][1][0],dot_pair)
					(out_info,in_info)=rm_link(node,out_info[orient][node][0][0],orient,out_info,in_info)
					cut=1
					break
				elif (path1.index(i)  >  path2.index(j)) or (path1.index(i) == path2.index(j) and cal_path_length(path1) > cal_path_length(path2)) : # path1.index(i) >=  path2.index(j):  ###path1 includes more nodes than path2 ## two paths include same node.  so comapre the lengths of two paths.
					dot_pair=rm_dotpair(node,out_info[orient][node][1][0],dot_pair)
					dot_pair=add_dotpair(node,out_info[orient][node][0][0],dot_pair)
					(out_info,in_info)=rm_link(node,out_info[orient][node][1][0],orient,out_info,in_info)
					cut=1
					break
		if cut:
			break
	return(out_info,in_info,dot_pair,cut)

def get_path(node,in_info,out_info,used_node):
	print('get_path',node)
	(node,orient,fpath,used_node)=walk_node(node,in_info,out_info,'+',used_node,100,0)   ### the forward path
	(node,orient,rpath,used_node)=walk_node(fpath[-1][0],in_info,out_info,rever_ori[fpath[-1][1]],used_node,100,0)  ### the  reverse path
	if len(fpath) < len(rpath):
		newpath=rpath
	else:
		newpath=fpath
	print(fpath,rpath)
	return(newpath,used_node)

change_tip=1
change_bubble=1
init_ori=['+','-']
while change_tip+change_bubble:  ####IF dot_pair is unchanged,  the graph is fixed.
	print('run')
	os.system('date')
	change_tip=0
	change_bubble=0
	used_node={}
	for node in node_list:
		for orient in ['+','-']:
			if node+orient in used_node :
				continue
			A=node
			(B,orient,path,used_node)=walk_node(A,in_info,out_info,orient,used_node,100,0)
			if len(in_info[orient][B]) >=2 and path[-1][0]!=B:  ###if in_num >1; if a single node with more than 1 input, ignore it.###A!=B to avoid the case that the in_num of the initial node is >1.
				A=path[-1][0]
				cut_flag=0
				for in_n in in_info[orient][B]:
					if B+'/'+in_n[0] not in dot_pair:
						cut_flag=1
				###if B+'/'+A not in dot_pair:
				if cut_flag:  #### B has more than one input node. there is one node pair that only in_n->B, but not B->in_n. it's a tip.
					used_tmp=used_node.copy()
					(out_info,in_info,dot_pair,virtual_dotpair,change)=cut_tip(A,B,orient,out_info,in_info,used_tmp,dot_pair,virtual_dotpair)  ##the orient is for B input.
					if change:
						change_tip+=1
			if len(out_info[orient][B]) ==2: ###if out_num==2:
				used_tmp=used_node.copy()
				(out_info,in_info,dot_pair,change)=cut_bubble(B,orient,in_info,out_info,used_tmp,dot_pair)  ######inluding two steps: recognize a bubble and cut  the bubble.
				if change:
					change_bubble+=1
	print('Cut Tips',change_tip)
	print('Cut Bubble',change_bubble)
used_node={}
new_contig={}
id=1
for node in node_list:
	if node+'+' in used_node or node+'-' in used_node:
		continue
	(new_contig[id],used_node)=get_path(node,in_info,out_info,used_node)
	id+=1
for i in range(1,id):
	newconfa.write('>')
	sum1=0
	sum2=0
	for j in new_contig[i]:
		newconfa.write(j[0]+'/'+j[1]+'_')
		sum1+=(int(j[0].split('bp')[0].split('_')[-1]))
		sum2+=(int(j[2]))
	path_len=(sum1+sum2)
	newconfa.write('\t{0}\n'.format(path_len))
#for s in single_ctg:
#	path_len=int(s.split('bp')[0].split('_')[-1])
#	newconfa.write('>{0}/+\t{1}\n{2}\n'.format(s,path_len,'A'*path_len))
newconfa.close()

os.system('date')
