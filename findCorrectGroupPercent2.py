#! /usr/bin/env python
import sys
input = open(sys.argv[1])
in2 = open(sys.argv[2])
output = open(sys.argv[3],'w')

allRefSets = []
curSet = set()
for line in input:
	if "Group Num" in line:
		if len(curSet)>0:
			allRefSets.append(curSet)
			curSet = set()
		continue
	if "-----------" in line:
		continue
	curSet.add(line.strip())

if len(curSet)>0:
	allRefSets.append(curSet)
	curSet = set()
allOtherSets = []
curList = []
endOfFile = False
ungrouped = 0
for line in in2:
	if "OrthoGroup" in line:
		if len(curList)>0:
			allOtherSets.append(curList)
			curList = []
		if "Ungrouped" in line:
			endOfFile = True
		continue
	if "-----------" in line:
		continue
	if endOfFile:
		ungrouped +=1
		continue
	curList.append(line.split("\t")[1].strip())
if len(curList)>0:
	allOtherSets.append(curList)



currentHeaderNum = 1
oneHundred = 0
fission = 0
fusion =0
incomplete =set()
usedRef = set()
for myList in allOtherSets:
	allCorrect = dict()
	#curHeader = myList[0]
	#goodRefSet = set()
	num = 0
	for refSet in allRefSets:
		for curHeader in myList:
			if curHeader in refSet:
				if not num in allCorrect:
					allCorrect[num] = 0
				allCorrect[num] +=1
				#goodRefSet = refSet
				#print "found"
				#break
		num +=1
	#totalCorrect = 0
	#totalWrong = 0
	output.write("OrthoGroup " +str(currentHeaderNum) +":\n")
	print allCorrect
	for key in allCorrect:
		output.write("\tRef: " + str(key) + "\t" + str(allCorrect[key]) + " / " + str(len(allRefSets[key])) +"\n")
		if len(allCorrect) >1:
			fusion +=1
		elif allCorrect[key]==len(allRefSets[key]):
			oneHundred +=1	
		else:
			incomplete.add(key)
		if key in usedRef:
			if key in incomplete:
				incomplete.remove(key)
			fission +=1
		usedRef.add(key)
	output.write("\n")
	currentHeaderNum += 1
print incomplete
output.write("Number of Groups:\t" + str(currentHeaderNum-1) + "\n")
output.write("References:\t" + str(len(usedRef)) + "\n")
output.write("100%\t" + str(oneHundred) + "\n")
output.write("Fission\t" + str(fission) + "\n")
output.write("Fusion\t" + str(fusion) + "\n") #OrthoBench said fusion had to have at least 3 genes from other group. I say just one gene
output.write("Incomplete\t" + str(len(incomplete)) + "\n")
output.write("Ungrouped\t" + str(ungrouped) +"\n")
output.write("\n")
	


input.close()
in2.close()
output.close()
