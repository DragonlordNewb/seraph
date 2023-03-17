from seraph import utils

class Directive(utils.DataContainer, utils.Makeable):
	def __init__(self, *args, **kwargs):
		utils.DataContainer.__init__(self, *args, **kwargs)
		self._args = args
		self._kwargs = kwargs
		self.completed = False
		
	def duplicate(self) -> object:
		return 
