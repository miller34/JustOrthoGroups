#! /usr/bin/env python

import sys

expected = open(sys.argv[1],'r')
input = open(sys.argv[2],'r')
output = open(sys.argv[3],'w')


realGroups = dict()

key = ''
for line in expected:
	if line[0] !='	':
		line =line.strip()
		key= line
		continue
	line =line.strip()
	#genes = set(line.split('\t')[1:])
	genes = set(line.split('\t'))
	realGroups[key]=genes
expected.close()



actual = dict() #OG# --> [orthologs]
key = ''
value = []
for line in input:
	if line[0] =='-':
		continue
	info = line.split(" ")
	if info[0] =='OrthoGroup':
		if key != '':
			actual[key] = value
			key =''
			value =[]
		if len(info)==2:
			key = info[1].split(":")[0]
		else:
			break
		continue
	value.append(line.strip().split("\t")[1][1:])





input.close()
output.write(str(len(actual.keys())) +" Groups:\n")
totalFoundInOMA = 0
totalPossible = 0
for key in actual:
	output.write(key)
	values = actual[key]
	for oKey in realGroups:
		totalFound = 0
		totalNum = len(realGroups[oKey])
		oValues = realGroups[oKey]
		for v in oValues:
			if v in values:
				totalFound +=1
		if totalFound>0:
			totalFoundInOMA +=totalFound
			output.write("\t" + oKey + ":" + str(totalFound) + "\\" + str(totalNum))
	output.write("\n")
	
for x in realGroups.values():
	totalPossible +=len(x)
output.write("Total Found: " + str(totalFoundInOMA) + "\nTotal Possible: " + str(totalPossible) +"\n")


output.close()



