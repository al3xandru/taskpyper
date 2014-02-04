#!/usr/bin/env python

""" Tool for checking off tasks based on text matching."""

import re;
from optparse import OptionParser
from sys import stdout,stderr
from datetime import datetime

from taskpyper import TaskFile


gDebug = True;
__version__  = u"0.1.0.6"

#:todo: hide this function from the outside world
def debugprint(*stuffToPrint):
	#Astric indicates that it can handle a list as input
	if (gDebug):
		print "DEBUG:" + " ".join(stuffToPrint)



def main():
	from optparse import OptionParser;

	importFilename = "test.taskpaper"
	tpBlob = None
	taskTextToFind = None	
	debugprint('main function of taskDone')
	
	
	#Parse for cmd line values
	optParser = OptionParser()
	optParser.add_option('-i','--inputFilename',dest='filename',help='input file',type='string')
	optParser.add_option('-t','--taskText',dest ='taskText', help='text_to_match',type='string')
	
	debugprint('parsing')
	(option, arg) = optParser.parse_args();

	if(option.filename and option.filename != ""):
		importFilename = option.filename;
		debugprint('import filename')
	if(option.taskText and option.taskText != ""):
		taskTextToFind = option.taskText


	#do something based on the settings
	if(importFilename):
		tpBlob =  TaskFile(importFilename)

	if tpBlob and (taskTextToFind is not None):
		debugprint('trying to match')
		matchedArray = tpBlob.findTaskByMatching(taskTextToFind)
		print ("== Found %02d Matches ==" % len(matchedArray))
#		dueItems = tpBlob.findDue(targetDatetime)
#		if(exportDueType == "stdout"):
#			print "Due Items:"
	else:
		print "No task to check-off has been specified"

if __name__ == u"__main__":
	main()
