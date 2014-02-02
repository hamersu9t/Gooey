'''
Created on Jan 24, 2014

@author: Chris
'''

import os
import wx 
import sys
import argparse 
import source_parser
from app.dialogs.config_model import ConfigModel
from app.dialogs import window
from app.dialogs.base_window import BaseWindow
from app.dialogs.advanced_config import AdvancedConfigPanel
from app.dialogs.basic_config_panel import BasicConfigPanel
from model.i18n import I18N
from functools import partial


def Gooey(f=None, advanced=False, language='english', noconfig=False):
	'''
	Decorator for client code's main function. 
	Entry point for the GUI generator.  
	
	Scans the client code for argparse data. 
	If found, extracts it and build the proper 
	configuration page (basic or advanced). 
	
	Launched 
	
	'''
	params = locals()
	for k,v in params.iteritems(): 
		print k, v
	def build(f):
		def inner():
			module_path = get_caller_path()
			try:
				parser = source_parser.extract_parser(module_path)
			except source_parser.ParserError:
				raise source_parser.ParserError(
																'Could not locate ArgumentParser statements.'
																'\nPlease checkout github.com/chriskiehl/gooey to file a bug')
			model = ConfigModel(parser) 
			if advanced:
				BodyPanel = partial(AdvancedConfigPanel, model=model) 
			else:
				BodyPanel = BasicConfigPanel
			
			app = wx.App(False)  
			frame = BaseWindow(BodyPanel, model, f, params)
			frame.Show(True)     # Show the frame.
			app.MainLoop() 

		inner.__name__ = f.__name__ 
		return inner

	if callable(f):
		return build(f)
	return build

def get_program_name(path):
	return '{}'.format(os.path.split(path)[-1])
	

def get_caller_path():
	# utility func for decorator
	# gets the name of the calling script
	tmp_sys = __import__('sys')
	return tmp_sys.argv[0]


if __name__ == '__main__':
	pass				