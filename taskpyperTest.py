#!/usr/bin/env python

import unittest;
from taskpyper import *;


#These are semi-standard magic values to track module info
__license__ = u"LGPL"
__version__  = u"0.1.0.16";
__author__ = u"FarMcKon";

_gDebug = False;


class TestTask(unittest.TestCase):

	def setUp(self):
		pass
	
	def test_constructor(self):
		task = Task("some Task",["@home"])
		self.assertEquals(len(task.attribs), 1)
		self.assertEquals(task.attribs[0], "@home")
		self.assertEquals(task.taskText, "some Task")
		
	def test_from_raw_string(self):
		testTuple = (
#			#(rawString, (text, [attribs])
			("some task to do @home @computer",("some task to do",["@home","@computer"])),

		)
		for entry in testTuple:
			(input,(expectedText, expectedList)) = entry
			task = Task.from_raw_string(input)
			self.assertEquals(len(expectedList), len(task.attribs))
			self.assertEquals(expectedText, task.taskText)
			#print task
			
	def test_print(self):
		testTuple = (
#			#(rawString, (text, [attribs])
			("some task to do @home @computer","TaskObj:' some task to do '	attribs: ['@home', '@computer']"),

		)
		for entry in testTuple:
			(input,expected) = entry
			task = Task.from_raw_string(input)
			#print task
			self.assertEquals(expected, str(task))	
			
			
class TestTaskFileLoader(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def test_load(self):
		loader = TaskFileLoader("test.taskpaper")
		taskList = loader.get_tasks()
		

class TestTaskManager(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def test_build_taskMgr(self):
		t = TaskManager("test.taskpaper")
	
	def test_task_by_attrib(self):
		t = TaskManager("test.taskpaper")
		matches = t.tasks_by_attribs("@tag")
		self.assertEquals(len(matches),1)
#		print matches
		matches = t.tasks_by_attribs("tag")
		self.assertEquals(len(matches),1)
#		print matches
		matches = t.tasks_by_attribs(["tag",'date'])
		self.assertEquals(len(matches),1)

	def test_task_string_by_attribs(self):
		t = TaskManager("test.taskpaper")
		matches = t.task_strings_by_attribs("@tag")
		
	def test_task_by_smart_attribs(self):
		t = TaskManager("test.taskpaper")
#		matches = t.task_by_smart_attribs("@tag")
#		self.assertEquals(len(matches),1)
		matches = t.task_by_smart_attribs("@today")
		self.assertEquals(2, len(matches))
			

##:todo: hide this function from the outside world
#def debugprint(*stuffToPrint):
#	#Astric indicates that it can handle a list as input
#	if (_gDebug):
#		print "DEBUG:" + " ".join(stuffToPrint)
#		
#		
#class TaskBlogTest(unittest.TestCase):
#
#	def setUp(self):
#		debugprint("setup UnitTests");
#		
#	def tearDown(self):
#		debugprint("setup tearDown");
#
#
#	def testLoad(self):
#		blog = TaskFile("UnitTester.taskpaper")
#		self.assert_(blog.tasksRawText)
#		self.assert_(blog.sourceFilename)
#		self.assert_(blog.fileSynced)
#
#	def testEmpty(self):
#		debugprint("testEmpty");
#
if __name__ == '__main__':
    unittest.main()
