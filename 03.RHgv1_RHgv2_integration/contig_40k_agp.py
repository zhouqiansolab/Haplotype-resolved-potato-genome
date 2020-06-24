


import sys

f1=open(sys.argv[1])  ##input RH_gv1_contig.agp
f2=open(sys.argv[2])  ##Input length file of splited seq
f3=open(sys.argv[3],'w')   ##Output file
f3.write('#seq\tscaf\tstart\tend\tchr\tstart\tend\n')


contig_agp={}

for line in f1:
	line=line.split()
	contig_agp[line[0]]=line[1:]
f1.close()

for line in f2:
	line=line.split()
	scaf='_'.join(line[0].split('_')[:3])
	scaf_s=int(line[0].split('_')[3].split('-')[0])
	scaf_e=int(line[0].split('_')[3].split('-')[1])
	chr=contig_agp[scaf][0]
	chr_s=int(contig_agp[scaf][1])+scaf_s-1
	chr_e=int(contig_agp[scaf][1])+scaf_e-1
	f3.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(line[0],scaf,scaf_s,scaf_e,chr,chr_s,chr_e))
f2.close()
f3.close()

