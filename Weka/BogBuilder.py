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

from Weka.ArffBuilder import *
from Weka.ArffParser import *

class BogBuilder:
	
	def __init__(self):
		cf = ConfigFile()
		vocabPath = cf.GetConfig("VOCAB")
		senDataPath = cf.GetConfig("SENSDATA")
		wrtDataPath = cf.GetConfig("WRITINGDATA")

		self.__wd = WritingData()
		self.__sd = SensData()
		self.__vocab = Vocab()

		# load ..
		self.__wd.Read(wrtDataPath)
		self.__sd.Read(senDataPath)
		self.__vocab.Read(vocabPath)


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

		
		
	
	def GenerateBog_BeforeFilter(self, arffOut):
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
	bb = BogBuilder()
	bb.GenerateBog_BeforeFilter('/home/xj229/data/7nat_lvl123_6000each_bf.arff')
