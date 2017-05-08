#! /usr/bin/env python

output = open("fileForCompTime",'w')

for x in range(1000):
	output.write("testTime/" + str(x) + "\n")
output.close()
