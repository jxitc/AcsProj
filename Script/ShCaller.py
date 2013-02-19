'''
Created on 2013-2-15

@author: Xiao
'''

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Corpus'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Weka'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Util'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Script'))
sys.path.append(os.path.dirname(__file__))

import subprocess

from Util.Log import *

class ShCaller:
	"""
	Class to call Bash Shell
	"""
	def __init__(self):
		self.__lg = Log()
		
	def Call(self, cmdList):
		cmdStr = ' '.join(cmdList)
		print("Executing command:\n" + cmdStr)
		
		self.__lg.WriteLog(cmdStr)
		subprocess.call(cmdList, shell=True)
