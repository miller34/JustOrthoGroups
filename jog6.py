#! /usr/bin/env python
import sys
import gzip
from multiprocessing import Process, current_process, freeze_support, Pool
import argparse
import os
import collections as cl
from Bio.Seq import Seq
from Bio.Alphabet import generic_rna,generic_dna

def findOrthoGroup(allOrthologs,key,allOrthos):

	for oKey in allOrthologs[key]:
		if oKey in allOrthos:
			continue
		allOrthos.add(oKey)
		allOrthos = findOrthoGroup(allOrthologs,oKey,allOrthos)
	return allOrthos

def getAllSubSeq(input):
	sequence,dirOverlap = input
	allSub = set()
	for x in xrange(len(sequence)-dirOverlap+1):
		allSub.add(sequence[x:x+dirOverlap])
	return allSub

def parseArgs():
	parser = argparse.ArgumentParser(description='Find Orthologs in MultiSpecies FASTA file.')
	parser.add_argument("-i",help="Input Fasta Files",nargs='*',action="store", dest="input", required=False)
	parser.add_argument("-id",help="Input Directory with Fasta Files",action="store", dest="inputDir", required=False)
	parser.add_argument("-o",help="Output OrthoGroup File",action="store",dest="output", required=True)
	parser.add_argument("-t",help="Number of Cores",action="store",dest="threads",default=1,type=int, required=False)
	parser.add_argument("-d",help="Direct Overlap",action="store",dest="overlap",default=6,type=int, required=False)
	parser.add_argument("-c",help="Number of Occurances",action="store",dest="occurances",default=8,type=int, required=False)
	parser.add_argument("-dna",help="Flag for DNA sequences",action="store_true",dest="dna", required=False)
	parser.add_argument("-rna",help="Flag for RNA sequences",action="store_true",dest="rna", required=False)
	args = parser.parse_args()
	return args

def readInputFiles(args):
	threads = args.threads
	dirOverlap = args.overlap
	orthoGroup =0
	header = ""
	sequence = ""
	allInputFiles = []
	pool = Pool(threads)
	results = []
	curHeaderNum =1
	if args.input:
		allInputFiles = args.input
	elif args.inputDir:
		allFasta = []
		#for (x,y,f) in os.walk(args.inputDir):
		#	allFasta = f
		path = args.inputDir
		allFasta = os.listdir(path)
		if path[-1] != '/':
			path += '/'
		allInputFiles = [path +i for i in allFasta]
	else:
		print "--i or --id is required"
		sys.exit()
	for inputFile in allInputFiles:
		mySequences = []
		input = ""
		if inputFile[-3:] =='.gz':
			input = gzip.open(inputFile,'r')
		else:
			input = open(inputFile,'r')
		for line in input:
			if line[0] =='>':
				if sequence !="":
					#print sequence
					if args.dna:
						sequence = str(Seq(sequence,generic_dna).translate())
					if args.rna:
						sequence = str(Seq(sequence,generic_rna).translate())
					numToHeader[orthoGroup] = header
					mySequences.append((sequence, dirOverlap))
					orthoGroup +=1
				header = inputFile + "\t" + line
				curHeaderNum +=1
				sequence = ""
				continue
			sequence +=line.upper().strip()
		if sequence != "":
			if args.dna:
				sequence = str(Seq(sequence,generic_dna).translate())
			if args.rna:
				sequence = str(Seq(sequence,generic_rna).translate())
			numToHeader[orthoGroup] = header
			mySequences.append((sequence, dirOverlap))
			orthoGroup +=1
			sequence = ""
		temp =pool.map(getAllSubSeq,mySequences,chunksize=1)
		results += temp
		#print len(results)
		#print len(numToHeader)
		input.close()
	return results

def forPoolGroupings(zz):
	x,numOccurances =zz
	numInstances = len(results)
	returnStuff = []
	for y in xrange(x,numInstances):
		addThis = len(results[x] & results[y])
		if addThis>numOccurances:
			returnStuff.append((x,y))
	return returnStuff

def getGroupings(numToHeader,results,threads,numOccurances):
	groupings = []
	numInstances = len(results)
	pool = Pool(threads)
	myNums = []
	for x in xrange(numInstances):
		myNums.append((x,numOccurances))
	#print "HI"
	temp = pool.map(forPoolGroupings,myNums,chunksize=1)
	#print "HI"
	for q in temp:
		for z in q:
			if len(z)==0:
				continue
			groupings.append(z)
	return groupings

def writeToFile(numToHeader,outputFile,groupings):
	sys.setrecursionlimit(40000)
	output = open(outputFile,'w')
	currentGroup = 1
	allUsedHeaders = set()
	setOfGood = dict()
	for tuple in groupings:
		x,y = tuple
		if not x in setOfGood:
			setOfGood[x] = set()
		setOfGood[x].add(y)
		if not y in setOfGood:
			setOfGood[y] = set()
		setOfGood[y].add(x)
	for key in setOfGood:
		if key in allUsedHeaders:
			continue
		groupHeaders = {key}
		groupHeaders = findOrthoGroup(setOfGood,key,groupHeaders) 
		if len(groupHeaders)>1:
			output.write("OrthoGroup " + str(currentGroup) + ":\n")
			currentGroup +=1
			for y in groupHeaders:
				allUsedHeaders.add(y)
				output.write(numToHeader[y])
			output.write("-----------------------------\n")
	output.write("OrthoGroup Ungrouped Genes:\n")
	for x in setOfGood.keys():
		if x not in allUsedHeaders:
			output.write(numToHeader[x])
	output.close()

if __name__ =='__main__':
	freeze_support()
	args = parseArgs()
	numToHeader = dict()
	results = readInputFiles(args)
	groupings = getGroupings(numToHeader,results,args.threads,args.occurances)	
	writeToFile(numToHeader,args.output,groupings)

