# -*- coding: utf-8 -*-

'''
Created on 2013-1-31

@author: Xiao
'''

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Corpus'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Weka'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Util'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Script'))
sys.path.append(os.path.dirname(__file__))

from Corpus.WritingData import *
from Corpus.Vocab import *
from Corpus.SensData import *

from Util.Log import *
from Util.ConfigFile import *
from Util.PorterStemmer import *
from Util.Perfmon import *

from Weka.ArffBuilder import *
from Weka.ArffParser import *

from Script.WekaSh import *

class BogBuilder:
	
	def __init__(self):
		cf = ConfigFile()
		vocabPath = cf.GetConfig("VOCAB")
		senDataPath = cf.GetConfig("SENSDATA")
		wrtDataPath = cf.GetConfig("WRITINGDATA")

		self.__wd = WritingData()
		self.__sd = None #SensData()
		self.__vocab = None #Vocab()

		# load ..
		self.__wd.Read(wrtDataPath)
		#self.__sd.Read(senDataPath)
		#self.__vocab.Read(vocabPath)

		self.__ptStm = PorterStemmer()

		# Bog words settings from config file

		if cf.GetConfig("BOG_STEMMER") == 'TRUE':
			self.__isUseStemmer = True
		else:
			self.__isUseStemmer = False

		if cf.GetConfig("BOG_LOWER") == 'TRUE':
			self.__isToLower = True
		else:
			self.__isToLower = False

		if cf.GetConfig("BOG_ALPHANUMONLY") == 'TRUE':
			self.__isAlphaNumOnly = True
		else:
			self.__isAlphaNumOnly = False

		self.__minFreq = int(cf.GetConfig("BOG_MINFREQ"))
		

	def _getCvSplitRange(self, nFold, nData):
		# TODO
		assert(nFold <= nData)
		
		idxArray = []

		step = int(nData / nFold)
		startIdx = 0
		endIdx = 1

		for iFold in range(nFold - 1):
			endIdx = startIdx + step
			idxArray.append((startIdx, endIdx))
			startIdx = endIdx

		# for last fold
		idxArray.append((startIdx, nData))

		assert(len(idxArray) == nData)

		return idxArray
			
	
	def SplitCrossValidationData(self, oriArffFile):
		"""
		Split the original file to n-fold validation
		Simple version 
		"""

		cf = ConfigFile()
		nFold = int(cf.GetConfig("CVFOLD"))
		ratio = 1.0 / float(nFold)
		
		# analyse Arff file
		
		ap = ArffParser()	
		ap.Parse(oriArffFile)
		headerStr = ap.GetHeader()
		dataLines = ap.GetDataLines()
		nData = len(dataLines)
		
		cvRange = self.__getCvSplitRange(nFold, nData)

		for iFold in range(nFold):
			print("Generate fold %d" % iFold)
			fnTrn = oriArffFile + "_fold_%d_trn.arff" % iFold
			fnTst = oriArffFile + "_fold_%d_tst.arff" % iFold
			
			print("Start writing traning file: " + fnTrn)
			fwTrn = open(fnTrn, 'w')
			fwTrn.write(headerStr)

			for iPart in range(nFold):
				if iPart == iFold:
					continue
				# else write as training data
				sIdx = cvRange[iPart][0]
				eIdx = cvRange[iPart][1]
				idx = sIdx
				while idx < eIdx:
					fwTrn.write(nData[idx])
			
			print("Start writing testing file: " + fnTst)

			fwTrn = open(fnTrn, 'w')
			fwTrn.write(headerStr)
	
			sIdx = cvRange[iFold][0]
			eIdx = cvRange[iFold][1]
			idx = sIdx
			while idx < eIdx:
				fwTrn.write(nData[idx])

	def isAllNonASCII(self, string):
		return all(ord(c) >= 128 for c in string)

	def ProcessToken(self, tok):
		"""
		Process token, according to the configuration setting
		i.e. lower? stemmer? etc.
		"""

		tok = tok.strip()
		if tok == '':
			return None

		if self.isAllNonASCII(tok):
			#print tok
			return None
		
		# substitution some char
		
		if tok.find("'") != -1:
			tok = "'%s'" % tok.replace("'", r"\'")

		if tok.find('%') != -1:
			tok = "'%s'" % tok.replace("%", r"\%")

		if self.__isToLower:
			tok = tok.lower()

		if self.__isUseStemmer:
			tok = self.__ptStm.stem(tok, 0, len(tok) - 1)

		if self.__isAlphaNumOnly:
			if not tok.isalnum():
				return None

		return tok


	def GetBog(self, sensDataPath, outBogPath):
		"""
		Generate weka format arff
		Will scan the sentence on the run!
		"""

		#Some bog setting
		lg = Log()
		msg = "BogBuilder.GetBog(\n%s ->\n %s" % (sensDataPath, outBogPath)
		print(msg)
		lg.WriteLog(msg)
		
		wd = self.__wd

		if wd is None:
			wd = WritingData()
			wd.Read()

		sd = self.__sd
		if sd is None:
			sd = SensData()
			sd.Read(sensDataPath)

		sensDict = sd.GetSensDict()

		# 1st pass
		# Building vocabulary
		# Get all the sentence first, establish the vocab

		vocab = {}
		classSet = set()
		classColStr = "Nationality"
		for wrtId in sensDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, i.e. nationality
			classVal = classVal.lower()
			classSet.add(classVal)

			sensList = sensDict[wrtId]
			for sen in sensList:
				toks = sen.split(' ')
				
				for tok in toks:
					# start adding to vocabulary
					
					tok = self.ProcessToken(tok)

					if tok is None or tok == '':
						continue
				
					if vocab.has_key(tok):
						vocab[tok] += 1
					else:
						vocab[tok] = 1


		relString = "BogBuilder -stmmer:%r -lower:%r -minFreq:%d -alphanumonly:%r" % \
							  (self.__isUseStemmer, self.__isToLower, \
								self.__minFreq, self.__isAlphaNumOnly)
								
		msg = "[BogBuilder] " + "First pass vocab scan, #vocab = %d" % len(vocab)
		print(msg)
		print(relString)
		lg.WriteLog("BOG setting: " + relString)
		lg.WriteLog(msg)

		# Further process vocabulary, i.e. min frequency cut-off

		# impose min word frequency cut-off
		if self.__minFreq > 1:
			for word in vocab.keys():
				freq = vocab[word]
				if freq < self.__minFreq:
					del vocab[word]

		msg = "[BogBuilder] " + "Applied minimum frequency cut-off (#attr) #vocab = %d" % len(vocab)
		print(msg)
		lg.WriteLog(msg)

		import operator
		sortedVocab = sorted(vocab.iteritems(), key = operator.itemgetter(1), reverse = True)
		
		bogAttrIdx = {}
		idx = 0
		for (word, freq) in sortedVocab:
			bogAttrIdx[word] = idx
			idx += 1

		# 2nd Pass
		# Start buiilding BOG!

		# Start writing ARFF file
		ab = ArffBuilder()
		ab.StartWriting(outBogPath)

		
		relString = "BogBuilder -stmmer:%r -lower:%r -minFreq:%d -alphanumonly:%r" % \
							  (self.__isUseStemmer, self.__isToLower, \
								self.__minFreq, self.__isAlphaNumOnly)

		ab.WriteRelation("text_file") # TODO!


		strNatClasses = "{"
		for n in list(classSet):
			if n == "":
				continue
			strNatClasses += "%s," % n
		strNatClasses = strNatClasses[0:-1] + "}"
		ab.AddAttr(classColStr, strNatClasses)

		# add other bog attributes
		for (word, freq) in sortedVocab:
			ab.AddAttr(word, 'numeric')

		ab.WriteAttr()
		



		# OK Finally, start writing data!

		# classColStr = "Nationality"
		bogAttrIdxOffset = 1
		nSen = 0
		for wrtId in sensDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, i.e. nationality

			if classVal is None:
				continue


			for sen in sensDict[wrtId]:
				# process each sentence

				attrList = []
				attrList.append('%d %s' % (0, classVal))

				toks = sen.split(' ')
				attrUnsort = set()
				for tok in toks:
					tok = self.ProcessToken(tok)
					
					if not bogAttrIdx.has_key(tok):
						continue
					
					attrIdx = bogAttrIdx[tok] + bogAttrIdxOffset
					attrUnsort.add(attrIdx)
				
				if len(attrUnsort) <= 0:
					continue
				
				attrSort = list(attrUnsort)
				attrSort.sort()
				
				for attrIdx in attrSort:
					attrList.append('%d %d' % (attrIdx, 1)) 

				ab.AddDataSparse(attrList)
				nSen += 1

		#Done! write summary
		msg = "Done! Number of instance wrote: %d" % nSen
		print(msg)
		lg.WriteLog(msg)
			
	
	def GenerateBog_Bef(self,arffOut):
		"""
		Generate bog arff file, before filter
		like ...

		"some text ...", classid
		"some text ...", classid
		"some text ...", classid
		"some text ...", classid

		"""
		
		wd = self.__wd
		sd = self.__sd
		sd.ResetWritingIter()
		vocab = self.__vocab
		
		ab = ArffBuilder()
		ab.StartWriting(arffOut)
		ab.AddAttr("text", "String")
		
		# Write arff header part
		strNatClasses = "{"
		for n in wd.GetUniqueData("Nationality"):
			if n == "":
				continue
			strNatClasses += "%s," % n
		strNatClasses = strNatClasses[0:-1] + "}"
		ab.AddAttr("nationality", "{fr,cn,mx,it,ru,de,br}") # TODO this is hack!

		ab.WriteRelation("text_files")
		ab.WriteAttr()


		# Write arff data part
		
		sens = sd.GetAllSentencesWrtId()

		for (wrtId, sen) in sens:
			nat = wd.GetValueByWid(wrtId, "Nationality")
					
			if nat == None:
				continue
			
			if nat.strip() == "":
				continue
			
			nat = nat.lower().strip()

			attrList = ['"%s"' % sen, nat]
			ab.AddData(attrList)
			
		

if __name__ == '__main__':
	pfm = Perfmon()
	
	pfm.Start()
	
	bb = BogBuilder()
	#bb.GenerateBog_BeforeFilter('/home/xj229/data/7nat_lvl123_6000each_bf.arff')

	iSenFile = '/home/xj229/data/7nat_lvl123_6000each.sen'
	oArffFile = '/home/xj229/data/7nat_lvl123_6000each.bog_M5_L_STM_ALPHANUM.arff'
	bb.GetBog(iSenFile, oArffFile)

	# Covert arff to libsvm
	ws = WekaSh()

	import os
	(fn,ext) = os.path.splitext(oArffFile)
	oLibSVMFile = fn + ".libsvm"
	ws.LibSVMSaver(oArffFile, oLibSVMFile)
		
	
	pfm.Stop()
	msg = pfm.GetSummary()
	
	print(msg)
	lg = Log()
	lg.WriteLog(msg)
