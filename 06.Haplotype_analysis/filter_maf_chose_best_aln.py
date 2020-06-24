import sys

f1=open(sys.argv[1])  ##input maf
f2=open(sys.argv[2],'w')   #output flt.maf

que_aln={};ref_aln={}
for line in f1:
	if '# identity=' in line:
		iden=line.split()[-1][1:-2]
		ref=''
	if 's' ==line[0] and ref=='':
		line=line.split()
		ref=line[1]
		if ref not in ref_aln:
			ref_aln[ref]=[]
		ref_aln[ref].append([int(line[2]),int(line[3]),iden])
	elif 's' ==line[0] and ref!='':
		line=line.split()
		que=line[1]
		if que  not in que_aln:
			que_aln[que]=[]
		que_aln[que].append([int(line[2]),int(line[3]),line[4],int(line[5]),iden])

for ref in ref_aln:
	ref_aln[ref].sort()
	flt_ref_aln=ref_aln[ref][:]  ##a hard copy
	for i in range(0,len(ref_aln[ref])-1):
		si=ref_aln[ref][i][0]
		ei=ref_aln[ref][i][0]+ref_aln[ref][i][1]
		for j in range(i+1,len(ref_aln[ref])):
			sj=ref_aln[ref][j][0]
			ej=ref_aln[ref][j][0]+ref_aln[ref][j][1]
			if (ei-si) + (ej-sj) -(max(ei,ej)-min(si,sj)) > min(ei-si,ej-sj)*0.3 : ##the overlap is larger than the one third of the smaller alignment.
				if max(ei-si,ej-sj) > 1.1*min(ei-si,ej-sj):
					if ei-si < ej-sj:
						if ref_aln[ref][i] in flt_ref_aln:
							flt_ref_aln.remove(ref_aln[ref][i])  ##remove the smaller alignment
							print("bad",ref_aln[ref][i],"good",ref_aln[ref][j])
					else:
						if ref_aln[ref][j] in flt_ref_aln:
							flt_ref_aln.remove(ref_aln[ref][j])
							print("good",ref_aln[ref][i],"bad",ref_aln[ref][j])
				else:
					if round(float(ref_aln[ref][i][-1]),1) < round(float(ref_aln[ref][j][-1]),1):  ##compare the identity
						if ref_aln[ref][i] in flt_ref_aln:
							flt_ref_aln.remove(ref_aln[ref][i])  ##remove the smaller alignment
							print("bad",ref_aln[ref][i],"good",ref_aln[ref][j])
					else:
						if ref_aln[ref][j] in flt_ref_aln:
							flt_ref_aln.remove(ref_aln[ref][j])
							print("good",ref_aln[ref][i],"bad",ref_aln[ref][j])
			elif  (ei-si) + (ej-sj) -(max(ei,ej)-min(si,sj)) <0:
				break
	ref_aln[ref]=flt_ref_aln[:]    # a hard copy


for que in que_aln:
	que_new=[]
	for pos in que_aln[que]:
		if pos[2]=='+':
			que_new.append(pos)
		else:
			start=pos[3]-pos[0]-pos[1]
			que_new.append([start,pos[1],'-',pos[3],pos[4]])
	que_new.sort()
	flt_que_aln=que_new[:]  ##a hard copy
	for i in range(0,len(que_new)-1):
		si=que_new[i][0]
		ei=que_new[i][0]+que_new[i][1]
		for j in range(i+1,len(que_new)):
			sj=que_new[j][0]
			ej=que_new[j][0]+que_new[j][1]
			if (ei-si) + (ej-sj) -(max(ei,ej)-min(si,sj)) > min(ei-si,ej-sj)*0.3 : ##the overlap is larger than the one third of the smaller alignment.
				if max(ei-si,ej-sj) > 1.1*min(ei-si,ej-sj):
					if ei-si < ej-sj:
						if que_new[i] in flt_que_aln:
							flt_que_aln.remove(que_new[i])  ##remove the smaller alignment
							print("bad",que_new[i],"good",que_new[j])
					else:
						if que_new[j] in flt_que_aln:
							flt_que_aln.remove(que_new[j])  ##remove the smaller alignment
							print("good",que_new[i],"bad",que_new[j])
				else:
					if round(float(que_new[i][-1]),1) < round(float(que_new[j][-1]),1):  ##compare the identity
						if que_new[i] in flt_que_aln:
							flt_que_aln.remove(que_new[i])  ##remove 
							print("bad",que_new[i],"good",que_new[j])
					else:
						if que_new[j] in flt_que_aln:
							flt_que_aln.remove(que_new[j])  ##remove 
							print("good",que_new[i],"bad",que_new[j])
			elif  (ei-si) + (ej-sj) -(max(ei,ej)-min(si,sj)) <0:
				break
	que_new=[]
	for pos in flt_que_aln:
		if pos[2] =='+':
			que_new.append(pos)
		else:
			start=pos[3]-pos[1]-pos[0]
			que_new.append([start,pos[1],pos[2],pos[3],pos[4]])   ##recover the  position in maf .
	que_aln[que]=que_new[:]    # a hard copy


f1.seek(0)
for line in f1:
	if '##maf' in line:
		f2.write(line)
		info=[]
		continue
	info.append(line)
	if '# identity=' in line:
		iden=line.split()[-1][1:-2]
		ref=''
		flag1=0; flag2=0
	elif 's' ==line[0] and ref =='':
		ref=line.split()
		if ref[1] in ref_aln:
			if [int(ref[2]),int(ref[3]),iden] in ref_aln[ref[1]]:
				flag1=1
	elif 's' ==line[0] and ref !='':
		que=line.split()
		if que[1]  in que_aln:
			if [int(que[2]),int(que[3]),que[4],int(que[5]),iden] in que_aln[que[1]]:
				flag2=1
		if flag1 and flag2:
			for i in info:
				f2.write(i)

		info=[]
f1.close()
f2.close()
