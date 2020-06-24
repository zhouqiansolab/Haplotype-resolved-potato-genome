#program name:connectsq.py
###program information###
#  version 1.0  author : zhouqian<zhouqian.sun@gmail.com>  date:2016.2.29

"""
   module  description
		version  author   date  
"""
# include the required module
import os 
import sys
import argparse


#command-line interface setting
parser=argparse.ArgumentParser(description='calculate sequence length in fa or fq file')
parser.add_argument('-i',type=argparse.FileType('r'),help='input file in .fa format')
parser.add_argument('-t',type=str,help='input file  format, fa or fq')
parser.add_argument('-o',type=argparse.FileType('w'),help='output file in tab split format')
args=parser.parse_args()

#class definition
def connectsq(input,output,type):

	if type=='fa':
		flag=0
		for line in input:
			if '>' in line and flag:
				output.write('{0}\t{1} bp\n'.format(name,len(newsq)))
				name=line.split()[0][1:]
				newsq=''
			elif '>' in line and flag==0:
				name=line.split()[0][1:]
				newsq=''
				flag=1
			elif '>' not in line:
				newsq+=line.strip()
		output.write('{0}\t{1} bp\n'.format(name,len(newsq)))
	elif type=='fq':
		flag=0
		for line in input:
			if '@' in line[0] and flag==4:
				output.write('{0}\t{1} bp\n'.format(name,len(newsq)))
				newsq=''
			if '@' in line[0] :
				flag=0
				name=line.strip()
			elif '@' not in line[0] and flag==1:
				newsq=line.strip()
			flag+=1
		output.write('{0}\t{1} bp\n'.format(name,len(newsq)))

if __name__=="__main__":
	connectsq(args.i,args.o,args.t)
	args.i.close()
	args.o.close()

