import sys
import os

f1 = open(sys.argv[1]) ## RH_DM_all_5.collinear_region.fil.sim.txt
file = open('lastz.sh','w')

for i in f1:
	i = i.strip().split()
	ID = i[1][:-1]
	cmd='awk \'{for (i=1;i<=NF; i++) if (i <7) printf $i" "; printf "\\n"}\''
	file.write('lastz {0}_2.fa {0}_1.fa --chain  --format=maf+  --matchcount=3000   --ambiguous=n| {1} >{0}.maf\n'.format(ID,cmd))
file.close
f1.close
