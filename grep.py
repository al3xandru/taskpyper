import re;


class grep():
	"""This is a qucik version of 'grep a list' I wrote for testing"""
	def __init__(self,*args):
		#print 'Foo'
		str = None
		target = None;
		matches = [];
		

		if(len(args) == 0):
			print 'No items! to search'
		if(len(args) >= 1):
			str = args[0];
		if(len(args) >= 2):
			target = args[1];
		
		#try to search for matches in the target	
		if (str is not None) and  (target is not None):
			reg = re.compile(re.escape(str),re.I)
			for item in target:
				if reg and (reg.search( item) is not None) :
					matches.append( item )
		
		if (matches is not None):
			print matches
	

		
def clear(size=50):
	"""quick function hack to clear the screen"""
	for i in range(0,size): print "";

	
def main():
	print 'main'
	
	#g = grep()


if __name__ == '__main__':
	main();
