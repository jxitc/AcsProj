'''
Created on 19 Feb 2013

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
from ShCaller import *

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


if __name__ == '__main__':
	ws = WekaSh()
	ipt = "../data/7nat_lvl123_6000each_bf.arff"
	opt = "../data/7nat_lvl123_6000each_bog.arff"

	ws.StringToWordVector(ipt,opt)

