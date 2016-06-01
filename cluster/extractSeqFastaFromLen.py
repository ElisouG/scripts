#!/usr/local/bioinfo/python/3.4.3_build2/bin/python
# -*- coding: utf-8 -*-
## @package extractSeqFastaFromLen.py
# @author Sebastien Ravel

##################################################
## Modules
##################################################
#Import MODULES_SEB
import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))+"/"
sys.path.insert(1,current_dir+'../modules/')
from MODULES_SEB import fasta2dict, lenSeq2dict, relativeToAbsolutePath

## Python modules
import argparse
from time import localtime, strftime
## BIO Python modules
from Bio import SeqIO

##################################################
## Variables Globales
version="0.1"
VERSION_DATE='31/03/2015'
debug="False"
#debug="True"


##################################################
## Main code
##################################################
if __name__ == "__main__":

	# Initializations
	start_time = strftime("%d-%m-%Y_%H:%M:%S", localtime())
	# Parameters recovery
	parser = argparse.ArgumentParser(prog='extractSeqFastaFromLen.py', description='''This Programme extract Fasta Seq with liste keep''')
	parser.add_argument('-v', '--version', action='version', version='You are using %(prog)s version: ' + version, help=\
						'display extractSeqFastaFromLen.py version number and exit')
	#parser.add_argument('-dd', '--debug',choices=("False","True"), dest='debug', help='enter verbose/debug mode', default = "False")

	files = parser.add_argument_group('Input info for running')
	files.add_argument('-f', '--fasta', metavar="<filename>", required=True, dest = 'fastaFile', help = 'fasta files')
	files.add_argument('-l', '--len', metavar="<int>", required=True, type = int, dest = 'lenSize', help = 'lensize cutoff')
	files.add_argument('-o', '--out', metavar="<filename>", required=True, dest = 'paramoutfile', help = 'Name of output file')
	files.add_argument('-k', '--keep', metavar="<g/greater/l/lower>", required=True, dest = 'keepValue',choices = ["g","greater","l","lower"], help = 'choice keep sequences size greater than -l (g/greater) or keep lower (l/lower)')

	# Check parameters
	args = parser.parse_args()

	#Welcome message
	print("#################################################################")
	print("#        Welcome in extractSeqFastaFromLen (Version " + version + ")          #")
	print("#################################################################")
	print('Start time: ', start_time,'\n')

	# Récupère le fichier de conf passer en argument
	fastaFile = relativeToAbsolutePath(args.fastaFile)
	outputfilename = relativeToAbsolutePath(args.paramoutfile)
	lenSize = args.lenSize
	keepValue = args.keepValue
	output_handle = open(relativeToAbsolutePath(outputfilename), "w")

	dicoSize = lenSeq2dict(fastaFile)
	dicoFasta = fasta2dict(fastaFile)

	nbKeep=0
	nbTotal = len(dicoFasta.keys())

	for ID in sorted(dicoSize.keys(), key=sort_human):
		lenSeq = dicoSize[ID]
		if keepValue in ["g","greater"]:
			if lenSeq >= lenSize:
				sequence = dicoFasta[ID]
				SeqIO.write(sequence,output_handle, "fasta")
				nbKeep += 1

		elif keepValue in ["l","lower"]:
			if lenSeq <= lenSize:
				sequence = dicoFasta[ID]
				SeqIO.write(sequence,output_handle, "fasta")
				nbKeep += 1



	print("\n\nExecution summary:")

	print("  - Outputting \n\
	Il y a au final %i Sequences garder sur les %i initial\n\
	les sequences sont ajouter dans le fichier %s" %(nbKeep,nbTotal,outputfilename))
	print("\nStop time: ", strftime("%d-%m-%Y_%H:%M:%S", localtime()))
	print("#################################################################")
	print("#                        End of execution                       #")
	print("#################################################################")
