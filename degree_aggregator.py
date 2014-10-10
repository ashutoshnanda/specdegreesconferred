import os
import glob
import re
import operator
#Filepath for all of the tsv files

"""
Returns a list of degree names and the number of times that they show up.
"""
def degree_aggregator(filepath="./data"):
	degreeDict = {}
	filesDir = glob.glob(filepath + "/*.tsv")
	for f in filesDir:
		openedFile = open (f, "r")

		for line in openedFile:
			degreeNameArray = re.split(r'\t+', line)
			degreeName = degreeNameArray[0]
			if degreeName != "NA":
				if degreeDict.has_key(degreeName):
					degreeDict[degreeName]+=1
				else:
					degreeDict[convert_to_standardized_string(degreeName)] = 1

	#returns a list of tuples with the first value being the key and the
	#second value being the value
	degreeList = sorted(degreeDict.items(), key=operator.itemgetter(0))
	return degreeList

"""
Returns a formatted representation of the degreeList
"""
def degree_dict_outputter(lst):
	for tup in lst:
		print tup[0] + ": " + str(tup[1])

"""
Converts string to lowercase and removes hyphens, ampersands and whitespace
"""
def convert_to_standardized_string(str):
	#convert to lowercase
	newstr = str.lower()
	#take out whitespaces
	newstr = newstr.replace(" ", "")

	if "&" in newstr:
		newstr = newstr.replace("&", "and")
	elif "-" in newstr:
		newstr = newstr.replace ("-", "")

	return newstr


if __name__ == "__main__":
	#degree_aggregator()
    degree_dict_outputter(degree_aggregator())