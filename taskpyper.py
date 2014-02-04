#!/usr/bin/env python
"""
Taskpyper is a module of taskaper markup tools written in pthon.
TODO: Document what markup is acceptable here."""

import re;
from optparse import OptionParser;
from sys import stdout,stderr
from datetime import *

import os
import logging
import codecs

#These are semi-standard magic values to track module info
__license__ = u"LGPL"
__version__  = u"0.1.0.16";
__author__ = u"FarMcKon";

#Global values 
_gDebug = True;
# Create our logger 
_gLog = logging.getLogger('MyLogger')
_gLog.setLevel(logging.DEBUG)
#Create the output vector for the log
#_gLogHandler = logging.FileHandler('dbg_log.txt','a+','UTF-8')
_gLogHandler = logging.StreamHandler()
_gLog.addHandler(_gLogHandler)

_gLog.debug('======' + str(datetime.now()) )
_gLog.debug('Log Created on taskpyper load :' + str(datetime.now()) )


class TaskManager():
	"""
	This is a general manager for tasks. It 3 functions
	1. Load/Save tasks.
	2. Search/find/flag tasks
	3. Remove/update/etc/
	"""
	
	taskList = None
	comments = None
	lastSyncIn = None #datetime obj
	
	
	def __init__(self, taskSource = None):
		""" General init. taskSource is saved."""
		if (os.path.isfile(taskSource)):
			loader = TaskFileLoader(taskSource)	
			(self.taskList,self.comments) = loader.get_tasks_and_comments()
			self.lastSyncIn = loader.lastRead
	
	def tasks_by_attribs(self, attribs, union = False):
		"""This function find tasks by attribute strings.  Attribs can 
		be a single string, or a list of strings.  Union is true/false to 
		indiicateds if a union (or intersection) is returned. Defautls to intersection.
		Returns a list of Task objects."""
		#union = True = take the union of all attribs
		#union = false = take the join of 
		_gLog.debug("find_by_attrib")
		
		if(type(attribs) is not list):
			attribs = [attribs]
				
		retList = None
		
		for attribString in attribs:
			if(attribString[0] != '@'):
				attribString = '@'+ attribString

			newSet = filter(lambda task: attribString in task.attribs, self.taskList)			

			if(retList is None):
				retList = newSet
			if(union == True):
				toAdd = filter(lambda newTask: newTask not in retList , newSet)
				retList.extend(toAdd)
			else:
				retList = filter(lambda knownTask: knownTask in newSet , retList)
				

		return retList

	def task_strings_by_attribs(self, attribs):
		"""This function find tasks by attribute strings.  Attribs can 
		be a single string, or a list of strings.  Union is true/false to 
		indiicateds if a union (or intersection) is returned. Defautls to intersection.
		Returns a list of strings. """

		tasks = self.tasks_by_attribs(attribs)
		matchStrings = map(lambda task: task.console_str(), tasks)
		return matchStrings
	
	def ttask_strings_by_smart_attribs(self, attribs):
		"""This function find tasks by attribute strings.  Attribs can 
		be a single string, or a list of strings.  This function will smart
		search for ['today', 'tomorrow', 'thisweek','done'] by expanding those to 
		include patterns specific to that day/week/month and look for variations.
		Returns a list of strings. """
		tasks = self.task_by_smart_attribs( attribs )
		return map(lambda tsk: tsk.console_str(), tasks)
	
	def task_by_smart_attribs(self, attribs):
		"""This function find tasks by attribute strings.  Attribs can 
		be a single string, or a list of strings.  This function will smart
		search for ['today', 'tomorrow', 'thisweek','done'] by expanding those to 
		include patterns specific to that day/week/month and look for variations.
		Returns a list of Task objects."""
		_gLog.debug("task_by_smart_attribs")

		# -- turn into a list if not
		if(type(attribs) is not list):
			attribs = [attribs]
	
		attribGroups = [] # a list of list of 'magic' attribs
		for a in attribs:
			if(a[0] != '@'):
				a = '@'+ a
			if(a == '@today'):
				_gLog.debug("task_by_smart_attribs: updating '@today'")
				newGroup = ['@today']
				#generate and add date variants
				newTag = self.due_tag_by_datetime(datetime.now())
				newGroup.append(newTag)
				attribGroups.append(newGroup)
			elif(a == '@tomorrow'):
				newGroup = ['@tomorrow']
				#generate and add date variants
				tomorrow = datetime.now() + timedelta(days=1)
				newTag = self.due_tag_by_datetime(tomorrow)
				newGroup.append(newTag )
				attribGroups.append(newGroup)
#			elif(a == 'thisweek'):
#				#generate and add date variants
#				pass
#			elif(a == 'thismonth'):
#				#generate and add date variants
#				pass	
#			elif(a == 'done'):
#				#generate and add date variants
#				pass	
			else:
				attribGroups.append([a,])
	
		matches = None
		for group in attribGroups:
			_gLog.debug("task_by_smart_attribs: getting group:" + str(group))
			newMatches = self.tasks_by_attribs(group, union = True)
			# -- first match, setup matches
			if(matches is None):
				matches = newMatches
			# -- nth match. Limit matches to union
			else:
				matches = filter(lambda task: task in newMatches, matches) 
			return matches

	@classmethod
	def due_tag_by_datetime(cls,dt = None, resolution = 3):
		""" Function to generate a 'due by' tag for a specific date. 
		and returns. Returns a string."""
		if(type(dt) is not datetime):
			return ''
		timeTup = dt.timetuple()
		if(resolution == 3):
			absDateString = "@due"+ str((timeTup[0],timeTup[1],timeTup[2]))
		else :
			absDateString = "@due"+ str(timeTup)
		absDateString = absDateString.replace(', ','-') #change date formatting 
		
		return absDateString

	def update(self):
		_gLog.error("implement")
	
	def write_tasks(self, taskDest = None, mode = 'w'):
		""" Function writes out tasks. Now simply sends a task to console."""
		if (taskDes == "sys.stdout" or taskDest == 'stdout'):
			pass
		else:
			_gLog.error("only write to stdout for now");


class Task():
	""" This function """
	attribs = None
	taskText = None
	
	def __init__(self, taskText = None, attribs = None):
		"""General Init"""
		self.attribs = attribs
		self.taskText = taskText
	
	@classmethod
	def from_raw_string(cls,rawText = None):

		#split string into parts
		words = rawText.split()
		#simplistic version
		#:TODO: make smarter about embedded or multi space tags
		attribs = filter(lambda word: word[0] == '@', words)
		taskTextWords = filter(lambda word : word not in attribs, words)
		taskText = ' '.join(taskTextWords)
		return cls(taskText,attribs)
	
	def __str__(self):
		return ' '.join(['TaskObj:\'',str(self.taskText),'\'\tattribs:',str(self.attribs)])

	def console_str(self):
		words = [self.taskText,]#.extend(self.attribs)
		words.extend(self.attribs)
		return ' '.join( words )

class TaskFileLoader():

	""" Loader for Tasks stored in a file """
	readtime = None
	filename =  None
	lastRead =  None
	lastWritten = None

	def __init__(self, filename = None, encoding = u'UTF-8'):		
		if (os.path.isfile(filename)):
			self.filename = filename 
			self.encoding = encoding
		else:
			_gLog.error('Could not load file ' + str(filename) )


	def get_tasks(self, filename = None, encoding = None):
		(tasks,comments) = self.get_tasks_and_comments(filename,encoding)
		return tasks


	def get_tasks_and_comments(self, filename = None, encoding = None):	
		""" """
		# -- setup values and load defaults
		fileText = None
		tasks = None
		if(filename is None):
			filename = self.filename
		if(encoding is None):
			encoding = self.encoding
		
		# ==  if we are a file, load it 
		if (os.path.isfile(filename)):
			fileObj = codecs.open(filename, u'r', encoding )
			if(fileObj is not None):
				self.lastRead = datetime.now()
				fileText = fileObj.read()
				fileObj.close()
				del fileObj	
		
		# -- if we have any text, build objects from it
		if(fileText is not None):
			fileLines = fileText.splitlines()
			fileLines = filter(lambda string: string != '', fileLines)

			# -- strip out comments, process them
			comments = filter(lambda string: string[0] == '#', fileLines)

			# -- take all non-comment lines, conver them into task objects
			taskLines = filter(lambda string: string[0] != '#', fileLines)
			tasks = map(lambda string: Task.from_raw_string(string), taskLines)
		
		return (tasks, comments)

#
#class TaskFile():
#	""" TaskFile class is used to managed a group of tasks	stored in a file. It contains 
#	accessory functions to make managing that file eaiser	"""
#
#	tasksRawText = None;   #the raw text from the file
#	sourceFilename = None; #the source/destination file
#	fileSynced = None; 	   #flag if the rawText and sourceFile are in sync
#
#
#	def __init__(self,filename=None):
#		""" Create the TaskFile object from a file"""
#		self.load(filename)
#		
#
#	def load(self,filename):
#		""" Load a text file of tasks into this TaskFile object """
#		debugprint( 'creating task blob from %s' %filename)
#		
#		if filename is not None:
#			debugprint('Loading from file %(file)s' % {'file': filename})
#			fh = open(filename,'r')
#			if(fh):
#				self.tasksRawText = fh.read()	
#				self.sourceFilename = filename
#				self.fileSynced = True;
#				fh.close()
#				del fh;
#				stdout.write('file loaded OK');
#		else: #filename in not None
#			self.tasksRawText = None;
#			self.fileSynced = None;
#			stdout.write('no load file specified');
#						
#
#	def autobackup(self, backupFilename=None):
#		""" backup the objects rawText data to the given filename.  If no name is given, backup 
#		to an name autogenerated by the time the funciton is called. This does NOT set the sync
#		bit."""
#		if backupFilename is None:
#			now = datetime.now()
#			nowTxt = now.strftime("%Y.%m.%d.%H.%M.%S")
#			backFilename = self.sourceFilename + "." + nowTxt +".backup"
#			debugprint("autobackup filename" + backFilename)
#			fh = open(backFilename,"w+")
#			fh.write(self.tasksRawText)
#			fh.close();
#			del fh;
#
#	def removeExactMatch(self,exactTaskText):
#		"""IF the passed text EXACTLY matches a task,that task is removed from the internal 
#		rawText stream. fileSynced is set to false if any modification took place"""
#		if exactTaskText:
#			#if exactTaskText[-1] != '\n':
#			#	exactTaskText = exactTaskText
#			regger = re.compile(re.escape(exactTaskText));
#			#print 'exact task text: '+ exactTaskText
#			#print regger
#			match = regger.search(self.tasksRawText,re.M);
#			#print 'match: ' + str(match)
#			if (match):
#				print 'match found'
#				re.sub('',self.tasksRawText)
#				self.fileSynced = False;
#			else:
#				print 'no match found'
#			
#		else:
#			print "no text FAIL!"
#		#make sure we have an exact whole line match
#		#and nuke it from the lastRawRead
#		#tpBlob.removeExactMatch(taskMatches[0])
#
#
#	def findTaskByMatching(self,taskTextToFind):
#		"""Takes a string, tries to find all tasks that have that text in it, andthen returns an
#		array of all tasks that matched the line"""
#		debugprint( 'find task by text: %s' % taskTextToFind)
#		matchedLines = []
#		matchReg = re.compile(re.escape(taskTextToFind), re.I)
#		for x in self.tasksRawText.split('\n'):
#			if (matchReg.search(x) != None):
#				matchedLines.append(x)
#				
#		return matchedLines
#
#		
#
#	def findDue(self, targetDT,skipDoneTasks=True, lang="EN"):
#		""" This function scans for items due that match the @date with the ISO format date info 
#		matching the passed datetime (targetDT). If the targetDT is the same day as the current 
#		system information, @today, @tonight and other patterns are added to thet search."""
#		duePatterns = ["\s@due\s","\s@todo"]		
#		dueItems = []
#		#ISO pattern xxx.xx.xx or xxxx-xx-xx
#		todayDue = u"\s@due\(%(year)04d(-|.| )%(month)02d(-|.| )%(day)02d\)" %  \
#					{'year':targetDT.year, 'month':targetDT.month, 'day':targetDT.day}
#		duePatterns.append(todayDue)
#			
#		#if today is targetDT, add some extra patterns	
#		now = datetime.now()
#		if(targetDT.year == now.year and targetDT.month == now.month and targetDT.day == now.day):
#			duePatterns.extend([u"\s@today",u"\s@tonight"])
#
#		#local language pattern if we ahve it
#		duePatterns.append(u"\s@" +now.strftime("%A")+u"\S") #full day name
#		duePatterns.append(u"\s@" +now.strftime("%a")+u"\S") #abbr day name
#		
#		#if(isoWeekdaySets.has_key(lang)):
#		#	weekdays = isoWeekdaySets[lang]
#		#	if weekdays.has_key(now.isoweekday()) :
#		#		str = u"\s@" + weekdays[now.isoweekday()];
#		#		debugprint(str)
#		#		duePatterns.append(str)
#		#		*/
#
#		#:TODO: if tomorrow is targetDT, add some extra patterns
#			
#		#:TODO: if yesterday was targetDT, add some extra patterns
#
#
#		#serch for the matches
#		for task in self.tasksRawText.split('\n'):
#			negatorPattern = u"\s@done"
#			negatorReg = re.compile(negatorPattern)
#			#TODO add ability to grab 'sub-issues'
#			for pattern in duePatterns:
#				#print '  doing pattern %s' % pattern
#				dueReg = re.compile(pattern, re.I);
#				if(dueReg.search(task)):
#					if((skipDoneTasks == False) or (negatorReg.search(task) == None) ):
#						dueItems.append(task);
#						#prevIssueIndentLvl = X;
#						debugprint('due item found: %s' % task)
#						
#		#TODO: strip duplicats from dueItems
#		
#		return dueItems;
#
#	def findPastDue(self):
#		#import datetime;
#		#today = datetime.date.today()
#		dueWithDate = [];
#		for x in self.tasksRawText.split('\n'):
#			pastDueReg = re.compile(u"\s@due\([0-9]{4}-[0-9]{2}-[0-9]{2}\)");
#			if(pastDueReg.search(x)):
#				dueWithDate.append(x)
#				#print 'due found %s' % x
#
#	def setIsoDates( baseDateTime = datetime.now()):
#		"""This funciton scans the file for  all dates with @somedayname and 
#		converts them to @event(IsoDate) or @due (IsoDate)
#		"""
#		
#		debugprint("Boo")
#		
#	
##	def updateAutomatics(self):
##		print "Testing UpdateAutomatics"
##		x = self.findAutomatics()
#
##	def findAutomatics(self):
##		"""returns a list of automated items from the raw text"""
##		matchAutomatedTag = []
##		for x in self.tasksRawText.split('n'):
##			print 'bar'
##			autoReg = re.compile(ur"@auto",re.I);
##			z = autoReg.search(x)
##			print z
##			if(z):
##				print 'baz'
##				print 'automated item found %s' % x
##				for c in range(0,len(z.groups())) :
#				
##					print "Groups %d: %s " % c, z.groups(c) 
##				matchAutomatedTag.append(x)
##		return matchAutomatedTag
#
