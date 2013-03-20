import sys
sys.path.append('..')

from FeatureExtractorBase import *

from Corpus.DependData import *
from Corpus.WritingData import *

from Util.ConfigFile import *
from Util.Log import *

class DepdExtractor(FeatureExtractorBase):
	"""
	Extract bag-of-dependency fature
	"""

	Description = "DepdExtractor"

	
	def __init__(self):
		cf = ConfigFile()

		lg = Log()
		lg.PrintWriteLog("Depedancy extractor initlized!")

		self.__minFreq = int(cf.GetConfig("DEPDFE_MINFREQ"))

		self.__depdData = None

	def SetDependDataObj(self, dd):
		self.__depdData = dd

	
	def __processSingleInstance(self, dataStr):
		"""
		Extract ngram feature for single dataStr
		"""

		rsltList = [self.__depdData.GetDependName(d) \
							  for d in self.__depdData.SplitDenpStr(dataStr)]

		return rsltList

	def ExtractFeatureOnCorpus(self, dataDict):
		"""
		Extract POS ngram feature from tree dict
		"""
		
		wd = WritingData.GetInstance()

		# Step 1. First pass scan to get sorted vocab
		vocab = {} # POS vocab
		classSet = set()
		classColStr = "Nationality"
		numWrt = 0
		for wrtId in dataDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, i.e. nationality
			classVal = classVal.lower()
			classSet.add(classVal)

			numWrt += 1
			if numWrt % 500 == 0:
				print("Processed num writing = %d" % numWrt)

			dataList = dataDict[wrtId]

			for dataStr in dataList:
				fes = self.__processSingleInstance(dataStr) # features from this tree

				for fe in fes:
					if vocab.has_key(fe):
						vocab[fe] += 1
					else:
						vocab[fe] = 1


		lg = Log()
		msg = "[DepdExtractor] " + "First pass vocab scan, #vocab = %d" % len(vocab)
		lg.PrintWriteLog(msg)


		# Step 2. Sort vocab, and doing min frequency cut-off

		if self.__minFreq > 1:
			for key in vocab.keys():
				freq = vocab[key]
				if freq < self.__minFreq:
					del vocab[key]

		msg = "[DepdExtractor] " + \
					"Applied minimum frequency cut-off (#attr) #vocab = %d" % len(vocab)
		print(msg)
		lg.WriteLog(msg)

		import operator
		sortedVocab = sorted(vocab.iteritems(), key = operator.itemgetter(1), \
												 reverse = True)
		
		attrIdx = {} # Index for attributes, for later looking-up
		idx = 0
		for (word, freq) in sortedVocab:
			attrIdx[word] = idx
			idx += 1
		

		# Step 3. Second pass, extracting feature
		attrIdxOffset = 1 # Because the first attribute is "CLASS_LABEL", \
											# so we need to add this offset
		nSen = 0
		featureList = []

		for wrtId in dataDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, nationality

			if classVal is None:
				continue

			dataList = dataDict[wrtId]
			for dataStr in dataList:
				# process each sentence

				attrList = []
				attrList.append('%d %s' % (0, classVal)) # Add class id first

				fes = self.__processSingleInstance(dataStr) # features from this tree

				# TODO This is numeric version!!
				feDict = {}
				
				for fe in fes:
					if not attrIdx.has_key(fe):
						continue

					idx = attrIdx[fe] + attrIdxOffset
					if feDict.has_key(idx):
						feDict[idx] += 1.0
					else:
						feDict[idx] = 1.0

				if len(feDict) <= 0: # TODO maybe reserve empty instace for combination
					print("Extract 0 features for data: " + dataStr)
					featureList.append(attrList) # Only has one attr, i.e. the class id
					continue
				
				# Sort the attribute list, as required for Sparse Data format in Weka
				sortedFeDict = sorted(feDict.iteritems(), key = operator.itemgetter(0))
				
				
				# Write up atrribute list
				for (idx,freq) in sortedFeDict:
					attrList.append('%d %.1f' % (idx, freq))  # 1, means 'norminal'

				# Final step, adding to feautreList to return
				featureList.append(attrList)

		return (classSet, sortedVocab, featureList)

def main_test():

	td = DependData.GetInstance()
	#td = SenTreeData.GetInstance('/home/xj229/data/test_1000line.tree')
	treeDict = td.GetDict()

	nfe = DepdExtractor()
	nfe.SetDependDataObj(td)
	(clsSet, attrList, feList) = nfe.ExtractFeatureOnCorpus(treeDict)

	print attrList[1:10]
	print feList[1:10]

	arffPath = '/home/xj229/test/prodRule_bog.arff'
	nfe.OutputArffFile(arffPath, clsSet, attrList, feList, feType = 'numeric')

	libsvmPath = arffPath + ".libsvm"
	nfe.ConvertArff2Libsvm(arffPath, libsvmPath)
	
if __name__ == '__main__':
	import cProfile
	cProfile.run('main_test()')

