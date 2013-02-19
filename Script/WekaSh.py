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


		fixPara = "java -cp %s weka.filters.unsupervised.attribute." \
							"StringToWordVector -N 0 -i %s -o %s" \
							% (WekaSh.__wekaJar, inputArff, outputArff)


		
		# Start constructing sh command list
		cmdList = fixPara.split(' ')

		WekaSh.__shCaller.Call(cmdList)
		
		# add -tokenizer list
		# TODO also the token string
		# -tokenizer "weka.core.tokenizers.WordTokenizer -delimiters \" \\r\\n\\t.,;:\\\'\\\"()?!\""

		tokPara = r"""
		"weka.core.tokenizers.WordTokenizer -delimiters \" \\r\\n\\t.,;:\\\'\\\"()?!\""
		"""
		tokPara = tokPara.strip()
		cmdList.append('-tokenizer')
		cmdList.append(tokPara)

		
		# process valParas and bool Paras
		valParas = {"WEKA_SWV_WORDTOKEEP" : "W", \
								"WEKA_SWV_MINFREQ" : "M",	\
								"WEKA_SMV_STEMMER" : "stemmer" \
							 }

		for k in valParas.keys():
			cfVal = WekaSh.__cfg.GetConfig(k)
			paraStr = "-" + valParas[k]
			cmdList.append(paraStr)
			cmdList.append(cfVal)

		boolParas = {"WEKA_SWV_LOWER" : "L"}

		for k in boolParas.keys():
			cfVal = WekaSh.__cfg.GetConfig(k)
			if cfVal == "TRUE":
				paraStr = "-" + boolParas[k]
				cmdList.append(paraStr)
		
		print(cmdList)
		
		WekaSh.__shCaller.Call(cmdList)
		


if __name__ == '__main__':
	ws = WekaSh()
	ipt = "../data/7nat_lvl123_6000each_bf.arff"
	opt = "../data/7nat_lvl123_6000each_bog.arff"

	ws.StringToWordVector(ipt,opt)

