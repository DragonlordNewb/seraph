from seraph import utils

class Directive(utils.DataContainer, utils.Makeable):
	requires = {} # dict of {name: default}
	
	def __init__(self, *args, **kwargs):
		for key in self.requires.keys():
			if not key in kwargs.keys():
				kwargs[key] = self.requires[key]
				
		utils.DataContainer.__init__(self, *args, **kwargs)
		self._args = args
		self._kwargs = kwargs
		self.completed = False
		
	def duplicate(self) -> object:
		return self.make(*self._args, **self._kwargs)
	
	def execute(self) -> bool:
		raise SyntaxError("Can't execute a base Directive class - use a subclass.")
