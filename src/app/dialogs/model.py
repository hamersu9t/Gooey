'''
Created on Jan 23, 2014

@author: Chris
'''

import types
from app.dialogs.action_sorter import ActionSorter

class ArgumentError(Exception):
	pass

class Model(object):
	_instance = None
# 	def __new__(cls, *args, **kwargs):
# 		if not cls._instance: 
# 			cls._instance = super(Model, cls).__new__(
# 																		cls, *args, **kwargs)
# 		return cls._instance
	
	def __init__(self, parser=None):
		print parser
		self._parser = parser 
		self.description = parser.description
		
		
		self.action_groups = ActionSorter(self._parser._actions) 
		
		# monkey patch
		self._parser.error = types.MethodType(
																	self.ErrorAsString, 
																	self._parser)
		
		Model._instance = self
		print self
	def HasPositionals(self):
		if self.action_groups._positionals:
			return True
		return False
	
	def IsValidArgString(self, arg_string):
		if isinstance(self._Parse(arg_string), str):
			return False
		return True
	
	def _Parse(self, arg_string):
		try: 
			self._parser.parse_args(arg_string.split())
			return True
		except ArgumentError as e:
			return str(e)
		
	def GetErrorMsg(self, arg_string):
		return self._FormatMsg(self._Parse(arg_string))
		
	def _FormatMsg(self, msg):
		output = list(msg)
		output[output.index(':')] = ':\n '
		return ''.join(output)
	
	@staticmethod 
	def ErrorAsString(self, msg):
		'''
		Monkey patch for parser.error
		Returns the error string rather than 
		printing and silently exiting. 
		''' 
		raise ArgumentError(msg)
	
	@classmethod
	def GetInstance(cls):	
		return cls._instance



if __name__ == '__main__':
	import argparse_test_data 
	parser = argparse_test_data.parser 
	
	model = Model(parser)
	b = model.GetInstance()
	print model
	print b 
	print model == b
	
	
# 	print m2

	
	
	
