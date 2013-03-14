'''
Created on 19 Feb 2013

@author: xj229
'''

import sys,os
sys.path.append('../')
sys.path.append('./')

from Util.Log import *
from Util.ConfigFile import *
from Util.Perfmon import *

from ShCaller import *
from CvEvaluator import *

class WekaSh:
	"""
	Provide series of weka sh command
	"""

	# class static member, Log and ConfigFile
	__log = None
	__cfg = None
	__shCaller = None

	# system environment
	__wekaJar = "" 


	def __init__(self):
		"""
		Constructor
		"""
		if WekaSh.__log is None:
			WekaSh.__log = Log()

		if WekaSh.__cfg is None:
			WekaSh.__cfg = ConfigFile()

		if WekaSh.__shCaller is None:
			WekaSh.__shCaller = ShCaller()

		WekaSh.__wekaJar = WekaSh.__cfg.GetConfig("WEKAROOT") + "/weka.jar"

	def StringToWordVector(self, inputArff, outputArff):
		"""
		Apply StringToWordVector filter to inputArff
		http://weka.sourceforge.net/doc.dev/weka/filters/unsupervised/attribute/StringToWordVector.html
		"""

		cmdList = ['./StringToWordVector.sh']

		# add parameters one by one
		
		cmdList.append(WekaSh.__cfg.GetConfig("WEKA_SWV_WORDTOKEEP")) #$1

		if WekaSh.__cfg.GetConfig("WEKA_SWV_LOWER") == 'TRUE':
			cmdList.append('-L') #$2
			
		cmdList.append(WekaSh.__cfg.GetConfig("WEKA_SWV_STEMMER")) #$3
		cmdList.append(WekaSh.__cfg.GetConfig("WEKA_SWV_MINFREQ")) #$4

		cmdList.append(inputArff) #$5
		cmdList.append(outputArff) #$6

		cmdList.append(WekaSh.__wekaJar)
		
		print(cmdList)
		
		WekaSh.__shCaller.Call(cmdList)
		
	def LibSVMSaver(self, iArffFile, oLibSVMFile):
		msg = "Convert arff to libSVM file"
		print(msg)
		
		iniPara = "java -Xmx5000M -cp %s weka.core.converters.LibSVMSaver " \
							"-c first" % (WekaSh.__wekaJar)
		cmdList = iniPara.split(' ')
		
		cmdList.append('-i')
		cmdList.append(iArffFile)

		cmdList.append('-o')
		cmdList.append(oLibSVMFile)
		
		self.__shCaller.Call(cmdList)
	
	def RunEval(self, testSetPath):
		"""
		Run evaluation of libsvm
		
		java -Xmx15000M -cp weka.jar weka.classifiers.bayes.NaiveBayes -v \
  	-c first -x 4 -t ~/data/7nat_lvl123_6000each_bog.arff \
  	-d
		"""
		
		cvEval = CvEvaluator()

		(folderName, fName) = os.path.split(testSetPath)
		(fNameWoExt, ext) = os.path.splitext(testSetPath)
		(fName, extName) = os.path.splitext(fName)

		# Constructing command list
		nCvFold = WekaSh.__cfg.GetConfig("WEKA_CVFOLD")
		iniPara = "java -cp %s weka.classifiers.bayes.NaiveBayes -v " \
							"-c first -x %s" % (WekaSh.__wekaJar, nCvFold)
		cmdList = iniPara.split(' ')

		nbModelPath = fNameWoExt + ".nbmodel"

		cmdList.append('-t')
		cmdList.append(testSetPath)

			
		# Constructing redirecting log
		import time
		timeStamp = time.strftime("%y%m%d%H%M%S", time.localtime())
		rdFile = fName + ".wekaEval_%s.log" % timeStamp

		# Run
		#cmdList = "java -cp /home/xj229/tools/weka/weka.jar weka.classifiers.bayes.NaiveBayes -v -c first -x 4 -t /home/xj229/data/7nat_lvl123_6000each.bog_M10_L_STM.arff".split(' ')
		WekaSh.__shCaller.RedirectedCall(cmdList, rdFile)

		logRdFileFull = "/home/xj229/logs/" + rdFile
		getRslt = WekaSh.__shCaller.GetGrep('Classified', logRdFileFull)
		print(getRslt)
		lg = Log()
		lg.PrintWriteLog(getRslt)

		
		(dictPrecision, dictRecall, dictF1) =	cvEval.EvaluateLogFile(logRdFileFull)

		sumF1 = 0.0
		for f1 in dictF1.values():
			sumF1 += f1

		lg.PrintWriteLog("Final F1 = %.5f" % (sumF1 / len(dictF1)))


if __name__ == '__main__':
	ws = WekaSh()
	
	pfm = Perfmon()
	pfm.Start()
	
	
#	ipt = "../data/7nat_lvl123_6000each_bf.arff"
#	opt = "../data/7nat_lvl123_6000each_bog.arff"
#
#	ws.StringToWordVector(ipt,opt)

	testSet = "/home/xj229/data/7nat_lvl123_6000each.bog_M5_L.arff"
	ws.RunEval(testSet)
	
	pfm.Stop()
	msg = pfm.GetSummary()
	print(msg)
	lg = Log()
	lg.WriteLog(msg)
