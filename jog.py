#! /usr/bin/env python
import sys
import gzip
from multiprocessing import Process, Queue, current_process, freeze_support, Manager,Lock
from multiprocessing.dummy import Pool as ThreadPool
import argparse
import os
from Bio.Seq import Seq
from Bio.Alphabet import generic_rna,generic_dna
def findOrthoGroup(allOrthologs,key,allOrthos):

	for oKey in allOrthologs[key]:
		if oKey in allOrthos:
			continue
		allOrthos.add(oKey)
		allOrthos = findOrthoGroup(allOrthologs,oKey,allOrthos)
	return allOrthos

def addToSuffixArray(inputQueue,allDictionaries,dirOverlap, lock):
	sequence,orthoGroup = inputQueue.get()
	#print orthoGroup
	for x in range(len(sequence)):
		if x >(len(sequence)-dirOverlap):
			break
		keys = sequence[x:x+dirOverlap]
		lock.acquire()
		if not keys in allDictionaries:
			allDictionaries[keys] = [orthoGroup]
		else:
			oSet = allDictionaries[keys]
			#if orthoGroup in allDictionaries[keys]:
			#	print "OOOOOH"
			oSet.append(orthoGroup)
			allDictionaries[keys] = oSet
		lock.release()
	#print "I'm here",len(allDictionaries)
	return

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

def readInputFiles(args,allDictionaries):
	threads = args.threads
	inputQueue = Queue()
	outputQueue = Queue()
	lock = Lock()
	dirOverlap = args.overlap
	orthoGroup =1
	header = ""
	sequence = ""
	allInputFiles = []
	if args.input:
		allInputFiles = args.input
	elif args.inputDir:
		allFasta = []
		for (x,y,f) in os.walk(args.inputDir):
			allFasta = f
		path = args.inputDir
		if path[-1] != '/':
			path += '/'
		allInputFiles = [path +i for i in allFasta]
	else:
		print "--i or --id is required"
		sys.exit()
	for inputFile in allInputFiles:
		input = ""
		if inputFile[-3:] =='.gz':
			input = gzip.open(inputFile,'r')
		else:
			input = open(inputFile,'r')
		for line in input:
			if line[0] =='>':
				if sequence !="":
					if args.dna:
						sequence = str(Seq(sequence,generic_dna).translate())
					if args.rna:
						sequence = str(Seq(sequence,generic_rna).translate())
					numToHeader[orthoGroup] = header
					inputQueue.put((sequence,orthoGroup))
					orthoGroup +=1
					if inputQueue.qsize()==threads:
						size = inputQueue.qsize()
						lastProcesses = []
						for i in range(size):
							if inputQueue.qsize()>0:
								t = Process(target=addToSuffixArray, args=(inputQueue,allDictionaries,dirOverlap,lock))
								t.start()
								lastProcesses.append(t)
						for t in lastProcesses:
							t.join()
				header = line
				sequence = ""
				continue
			sequence +=line.upper().strip()
		if sequence != "":
			if args.dna:
				sequence = str(Seq(sequence,generic_dna).translate())
			if args.rna:
				sequence = str(Seq(sequence,generic_rna).translate())
			numToHeader[orthoGroup] = header
			inputQueue.put((sequence,orthoGroup))
			orthoGroup +=1
		size = inputQueue.qsize()
		lastProcesses = []
		for i in range(size):
			if inputQueue.qsize()>0:
				t = Process(target=addToSuffixArray, args=(inputQueue,allDictionaries,dirOverlap,lock))
				t.start()
				lastProcesses.append(t)
		for t in lastProcesses:
			t.join()
		input.close()


#def poolGroupings(x):
#		if len(allDictionaries[x])>1:
#			for y in allDictionaries[x]:
#				for z in allDictionaries[x]:
#					#lock.acquire()
#					if not z in groupings[y]:
#						groupings[y][z] = 0
#					groupings[y][z] +=1
#					#lock.release()
#
#		return
#
#def multArgsForPoolGroupings(args):
#	poolGroupings(*args)
#	return

def getGroupings(numToHeader,allDictionaries,threads):
	#pool = ThreadPool(threads)
	#lock = Lock()
	#manager = Manager()
	#groupings = manager.dict()
	groupings = dict()
	for key in numToHeader.keys():
		groupings[key] = dict()

	#pool.map(poolGroupings,allDictionaries.keys())
	for x in allDictionaries.values():
		if len(x)>1:
			for y in x:
				for z in x:
					if not z in groupings[y]:
						groupings[y][z] = 0
					groupings[y][z] +=1
	#for x in allDictionaries.keys():
	#	if len(allDictionaries[x])>1:
	#		for y in allDictionaries[x]:
	#			for z in allDictionaries[x]:
	#				if not z in groupings[y]:
	#					groupings[y][z] = 0
	#				groupings[y][z] +=1
	return groupings

def writeToFile(args,groupings):
	sys.setrecursionlimit(40000)
	output = open(args.output,'w')
	currentGroup = 1
	allUsedHeaders = set()
	setOfGood = dict()
	for key in groupings.keys():
		groupHeaders = set()
		for x in groupings[key]:
			if groupings[key][x]>numOccurances:
				groupHeaders.add(x)
		setOfGood[key] = groupHeaders
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
	for x in groupings.keys():
		if x not in allUsedHeaders:
			output.write(numToHeader[x])
	output.close()

if __name__ =='__main__':
	freeze_support()
	args = parseArgs()
	numToHeader = dict()
	manager = Manager()
	allDictionaries = manager.dict()
	readInputFiles(args,allDictionaries)
	numOccurances = args.occurances
	groupings = getGroupings(numToHeader,allDictionaries,args.threads)	
	
	writeToFile(args,groupings)

