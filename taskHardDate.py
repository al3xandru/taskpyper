#!/usr/bin/env python

""" Tool for converting a human date 'Wednesday' or 'next week' into a ISO date string"""

import re;
from optparse import OptionParser
from sys import stdout,stderr
from datetime import datetime

from taskpyper import TaskFile


gDebug = True;
__version__  = u"0.1.0.1"

#:todo: hide this function from the outside world
def debugprint(*stuffToPrint):
	#Astric indicates that it can handle a list as input
	if (gDebug):
		print "DEBUG:" + " ".join(stuffToPrint)



def main():
	from optparse import OptionParser;

	importFilename = "test.taskpaper"
	tpBlob = None
	debugprint('main function of exactDate')
	setIsoDates = True
	
	#Parse for cmd line values
	optParser = OptionParser()
	optParser.add_option("-i","--inputFilename",dest='filename',help="input file",type='string')

	
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
