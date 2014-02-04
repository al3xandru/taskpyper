#!/usr/bin/env python

""" Tool for Merging two task list files into one. It is a 'maximum merge' where any
addition to either file is preserved"""

def main():
	from optparse import OptionParser;

	tpBlob = None
	debugprint('main function of exactDate')	
	fileOne = None
	fileTwo = None
	
	#Parse for cmd line values
	optParser = OptionParser()
	optParser.add_option("-o","--fileOne",dest='fileOne',help="input file 1",type='string')
	optParser.add_option("-t","--fileTwoe",dest='fileTwo' ,help="input file 2",type='string')

	
	debugprint('parsing')
	(option, arg) = optParser.parse_args();

	if(option.filename and option.filename != ""):
		importFilename = option.filename;
		debugprint('import filename')

	if(importFilename):
		tpBlob =  TaskFile(importFilename)

	if tpBlob and (setIsoDates):
		
		#sets ISO dates based on the passed day
		dueTasks = tpBlob.setIsoDates()
#		if(exportDueType == "stdout"):
#			print "Due Items:"
#			for task in dueTasks:
#				print str(task)

if __name__ == u"__main__":
	main()
