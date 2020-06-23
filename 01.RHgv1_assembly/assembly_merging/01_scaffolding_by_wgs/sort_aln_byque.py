
import os
import re
import sys

f1=open(sys.argv[1])  ###input raw alignment file in the format of blasr m=5
f2=open(sys.argv[2],'w')   ### output sorted  file firstly by the query ID and  secondly by the position.

map={}
map_ref={}
for rawline in f1:
	line=rawline.split()
	#if int(line[11]) <1000:
	#	continue
	if line[0] not in map:
		map[line[0]]=[]
	map[line[0]].append(rawline)
	if line[5] not in map_ref:
		map_ref[line[5]]=[]
	map_ref[line[5]].append(rawline)
f1.close()

refs=list(map_ref.keys())
contig=list(map.keys())
contig.sort()
for c in contig:
	mapos={}
	for m in map[c]:
		mapos[m]=[int(m.split()[2]),int(m.split()[3]),m.split()[5]]   ### in case that one fragment of query mapped to two places on reference.
	pos=list(mapos.values())
	pos.sort()
	for p in range(0,len(pos)):
		for m in mapos:
			if mapos[m]==pos[p]:
				f2.write('{0}\n'.format(m.strip()))
f2.close()
f1.close()
