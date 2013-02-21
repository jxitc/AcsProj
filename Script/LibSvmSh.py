'''
Created on 21 Feb 2013

@author: xj229
'''

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Corpus'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Weka'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Util'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Script'))
sys.path.append(os.path.dirname(__file__))

from Util.Log import *
from Util.ConfigFile import *
from Util.Perfmon import *
from ShCaller import *

class LibSvmSh:
	"""
	Provide series of weka sh command
	"""

	# class static member, Log and ConfigFile
	__log = None
	__cfg = None
	__shCaller = None

	# system environment
	__libSvmFolder = "" 

	def __init__(self):
		"""
		Constructor
		"""
		if LibSvmSh.__log is None:
			LibSvmSh.__log = Log()
		
		if LibSvmSh.__cfg is None:
			LibSvmSh.__cfg = ConfigFile()
		
		if LibSvmSh.__shCaller is None:
			LibSvmSh.__shCaller = ShCaller()
      

	def RunEval(self, testSetPath):
		"""
		Run evaluation of libsvm
		"""
		
		svmRoot = LibSvmSh.__cfg.GetConfig("LIBSVM_ROOT")
		nFold = LibSvmSh.__cfg.GetConfig("LIBSVM_CVFOLD")
		iniPara = "%s/train -v %s %s" \
							% (svmRoot, nFold, testSetPath)

		cmdList = iniPara.split(' ')

		rdFile = '/home/xj229/data/a.log'
		LibSvmSh.__shCaller.RedirectedCall(cmdList, rdFile)
	
if __name__ == '__main__':
	pfm = Perfmon()
	
	pfm.Start()
	
	lss = LibSvmSh()
	fn = '/home/xj229/data/7nat_lvl123_6000each.bog_M5_L_STM.libsvm'
	lss.RunEval(fn)
	
	pfm.Stop()
	msg = pfm.GetSummary()
	
	print(msg)
	lg = Log()
	lg.WriteLog(msg)
