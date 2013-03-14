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
import time
import os.path
from threading import *

from Util.ConfigFile import *
from Util.Log import *

class ThreadFlag:
	"""
	Thread flag object
	"""
	def __init__(self):
		self.Flag = None

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

		subprocess.call(cmdList, shell=False)

	
	def __monitorAndPrint(self, rdFilePath, flag):
		"""
		Monitor a shell command redirected file, and output its value
		to stdout in realtime
		"""

		# Wait for file open first
		time.sleep(2)
		interval = 0.1
		while(True):
			if os.path.exists(rdFilePath):
				break

			if flag.Flag != 0:
				break
			else:
				time.sleep(interval)

		# Start monitor 
		print("Start monitoring file %s and output!" % rdFilePath)
		fr = open(rdFilePath, 'r')
		while(True):
			lines = fr.readlines()
			for line in lines:
				sys.stdout.write(line)

			if flag.Flag == 2: # == 2 meaning stopped writing
				break
			else:
				time.sleep(interval)

		print("Done! End monitoring!")
		

	def RedirectedCall(self, cmdList, rdFilePath):
		"""
		Call and redirect the stdout to rdFilePath
		"""

		# First, detect if rdFilePath cotains no path, then
		# re-set it under logs/ folder
		(folder, fileName) = os.path.split(rdFilePath)
		if folder == '':
			cf = ConfigFile()
			logFolder = cf.GetConfig("LOGFOLDER")
			rdFilePath = os.path.join(logFolder, fileName)

		cmdStr = ' '.join(cmdList)
		msg = "Executing command (redirect to file: %s):\n%s" % (rdFilePath, cmdStr)
		print(msg)
		self.__lg.WriteLog(msg)

		flagObj = ThreadFlag()

		# Start monitor thread
		monitorThread = Thread(target = self.__monitorAndPrint, \
													 args = (rdFilePath, flagObj))
		#monitorThread.start() # TODO

		# Execute command as usual
		fw = open(rdFilePath, 'w')
		subprocess.call(cmdList, stdout = fw, shell=False)
		fw.close()

		# Finished command, stop monitoring thread
		flagObj.Flag = 2

	def GetGrep(self, pat, file):
		"""
		Get the grep result 
		"""
		cmdList = []
		cmdList.append('grep')
		cmdList.append(pat)
		cmdList.append(file)

		# Python 2.6.8 can only use following:
		rslt = subprocess.Popen(cmdList, \
														stdout = subprocess.PIPE).communicate()[0]

		return rslt
		
