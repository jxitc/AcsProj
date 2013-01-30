'''
Created on 30 Jan 2013

@author: xj229
'''

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Corpus'))


class Log:
	"""
	Log class
	"""
	# class static variable
	RunLogFilePath = "" 
	RunLogWriter = None

	def __init__(self):
		if self.RunLogFilePath == "":
			self.RunLogFilePath = os.path.join(os.path.dirname(__file__), \
																				'../Run.log',)
		else:
			pass

		if self.RunLogWriter is None:
			self.RunLogWriter = open(self.RunLogFilePath, 'r')
		
		print("Start Logging")
			
	
