# File: readline-example-2.py
class Completer:
    def __init__(self, words):
        self.words = words
        self.prefix = None

    def complete(self, prefix, index):
        if prefix != self.prefix:
            # we have a new prefix!
            # find all words that start with this prefix
            self.matching_words = [
                w for w in self.words if w.startswith(prefix)
                ]
            self.prefix = prefix
        try:
            return self.matching_words[index]
        except IndexError:
            return None


class TaskCompleter(Completer):
	
	def __init__(self,words):
		Compeleter.__init__(self,words)


def main():
	i = CompleterInterface()
	i.setup()
	i.start_interactive_mode()
	
	
class CompleterInterface():

	completer = None;
	taskMgr = None
		
	def __init__(self):
		pass;
		
	def setup(self):

		# a set of more or less interesting words
		#words = 'load'
		#words = "perl", "pyjamas", "python", "pythagoras", 'exit'
		words = 'add','help','exit','load','listall','findby','save'

		print "Setting completer"
		self.completer = Completer(words)

		self.taskMgr = TaskManager("test.taskpaper")

	def start_interactive_mode(self):
		readline.parse_and_bind("tab: complete")
		readline.set_completer(self.completer.complete)

		while 1:
			inputBuffer = raw_input()
			if(inputBuffer == 'add'):
				print "useage: add the task text. Adds all text following 'add' as a task"			
			elif(inputBuffer.find('add') == 0):
				print 'add to tasks: \'' + inputBuffer[4:] + "'"
			elif(inputBuffer == 'help'):
				print 'print contextual help'
			elif(inputBuffer == 'exit'):	
				break;
			elif(inputBuffer.find('load') == 0):
				print 'load tasks here'
			elif(inputBuffer.find('listall') == 0):
				print 'load tasks here'
			elif( inputBuffer.find('findby ') == 0):
				line = inputBuffer[7:]
				items = self.taskMgr.text_task_by_smart_attribs(line)
				for i in items:
					print i
			elif( inputBuffer.find('save ') == 0):
				print 'you might want to save here'				
			else:
				print('unknown cmd>' + inputBuffer)
			print repr(raw_input(">>> "))

#import readline
try:
	import readline 
except ImportError: 
	print "Module readline not available." 
	import rlcompleter 
from taskpyper import *

if __name__ == '__main__':
	main()

