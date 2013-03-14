'''
Created on 21 Feb 2013

@author: xj229
'''

import sys,os
sys.path.append('../')

from Util.Log import *
from Util.ConfigFile import *
from Util.Perfmon import *
from Corpus.CvSplitter import *
from ShCaller import *
from Script.CvEvaluator import *

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
      

	def RunEval_Accuracy(self, testSetPath):
		"""
		Run evaluation of libsvm
		"""
		
		svmRoot = LibSvmSh.__cfg.GetConfig("LIBSVM_ROOT")
		nFold = LibSvmSh.__cfg.GetConfig("LIBSVM_CVFOLD")
		iniPara = "%s/train -v %s %s" \
							% (svmRoot, nFold, testSetPath)

		cmdList = iniPara.split(' ')

		(folderName, fName) = os.path.split(testSetPath)
		(fName, extName) = os.path.splitext(fName)
		import time
		timeStamp = time.strftime("%y%m%d%H%M%S", time.localtime())
		rdFile = fName + ".libsvmEval_%s.log" % timeStamp

		LibSvmSh.__shCaller.RedirectedCall(cmdList, rdFile)

		getRslt = LibSvmSh.__shCaller.GetGrep('Accuracy', "/home/xj229/logs/" + rdFile)
		print(getRslt)
		LibSvmSh.__log.WriteLog(getRslt)

	def RunEval(self, testSetPath):
		"""
		Run Evaluation of libsvm, with P/R/F
		"""
		
		lg = LibSvmSh.__log

		svmRoot = LibSvmSh.__cfg.GetConfig("LIBSVM_ROOT")
		nFold = int(LibSvmSh.__cfg.GetConfig("LIBSVM_CVFOLD"))
		
		cvSp = CvSplitter()
		nFoldList = cvSp.Split(testSetPath, nFold)

		if len(nFoldList) != nFold:
			print("Error in cross validation split")
			print(nFoldList)
			assert(0)

		cvEval = CvEvaluator()

		rsltFold = []
		totalAvgF1 = 0.0
		for i in range(nFold):
			(fnTrn, fnTst) = nFoldList[i]

			lg.PrintWriteLog("Fold %d Training: %s" % (i, fnTrn))

			# Step 1: get prediction on each data
			fnModel = fnTrn + ".model"
			fnPredict = fnTst + ".predict"

			trnPara = "%s/train %s %s" % (svmRoot, fnTrn, fnModel)
			trnCmdList = trnPara.split(' ')
			LibSvmSh.__shCaller.Call(trnCmdList)

			lg.PrintWriteLog("Fold %d Predicting: %s" % (i, fnTrn))
			predPara = "%s/predict %s %s %s" % (svmRoot, fnTst, fnModel, fnPredict)
			predCmdList = predPara.split(' ')
			LibSvmSh.__shCaller.Call(predCmdList)
			
			
			# Step 2: running statistics on predicted data, to get PRF
			(dictP, dictR, dictF) = cvEval.Evaluate(fnTst, fnPredict)

			allF1 = sum(dictF.values())
			avgF1 = float(allF1) / float(len(dictF))
			lg.PrintWriteLog("Got evaluation for current fold, Avg. F1 = %.5f" % avgF1)

			totalAvgF1 += avgF1
			

			rsltFold.append((dictP, dictR, dictF))

		# OK do statistics
		AvgAvgF1 = totalAvgF1 / float(nFold)
		lg.PrintWriteLog("Evaluation Done! Final after %d-fold Avg. F1 = %.5f" \
										 % (nFold, AvgAvgF1))

		

	
if __name__ == '__main__':
	pfm = Perfmon()
	
	pfm.Start()
	
	lss = LibSvmSh()
	fn = '/home/xj229/data/3nat_lvl123_15K.bog_M5_L.libsvm'

	lss.RunEval(fn)
	
	pfm.Stop()
	msg = pfm.GetSummary()
	
	print(msg)
	lg = Log()
	lg.WriteLog(msg)

