import sys
sys.path.append('..')

from FeatureExtractorBase import *

from Corpus.SenTreeReader import *
from Corpus.SenTreeData import *
from Corpus.WritingData import *

from Util.ConfigFile import *
from Util.Log import *

class ProdRuleExtractor(FeatureExtractorBase):
	"""
	Extract bag-of-production-rule fature
	"""

	Description = "ProdRuleExtractor"

	
	def __init__(self):
		cf = ConfigFile()
		self.__ngramN = int(cf.GetConfig("PRODRULE_N"))

		lg = Log()
		lg.PrintWriteLog("ProdRule Feature Extractor initialized, n = %d" \
											% self.__ngramN)

		self.__nGramMinFreq = int(cf.GetConfig("PRODRULE_MINFREQ"))

		self.__useExactNgram = True # Extract only exact the N ngram
																# will not continue extract N-1, N-2 ... etc

		self.__treeReader = SenTreeReader()

		
	def __getNgramStr(self, listObjs):
		"""
		Concatenate all elements in list to a string
		"""
		l = list(listObjs)
		strJoin = '|'
		return strJoin.join([str(s) for s in l])

	def __processToken(self, tok):
		"""
		Processing token, for example, substitute , with _COMMA_
		"""
		
		tok = tok.replace(',', '_COMMA_')
		tok = tok.replace("''", '_QUOTE*2_')

		return tok
		
	def __processSingleInstance(self, treeStr):
		"""
		Extract ngram feature for single treeStr
		"""

		tr = self.__treeReader
		(rootNode, terminalNodes) = tr.Scan(treeStr)
		rsltProdRuleList = [self.__processToken(r) \
												for r in tr.GetProdRuleList(rootNode)]

		tr.Destroy(rootNode)

		return rsltProdRuleList

	def ExtractFeatureOnCorpus(self, treeDict):
		"""
		Extract POS ngram feature from tree dict
		"""
		
		wd = WritingData.GetInstance()

		# Step 1. First pass scan to get sorted vocab
		vocab = {} # POS vocab
		classSet = set()
		classColStr = "Nationality"
		numWrt = 0
		for wrtId in treeDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, i.e. nationality
			classVal = classVal.lower()
			classSet.add(classVal)

			numWrt += 1
			if numWrt % 500 == 0:
				print("Processed num writing = %d" % numWrt)

			treeList = treeDict[wrtId]

			for treeStr in treeList:
				fes = self.__processSingleInstance(treeStr) # features from this tree

				for fe in fes:
					if vocab.has_key(fe):
						vocab[fe] += 1
					else:
						vocab[fe] = 1


		lg = Log()
		msg = "[ProdRuleFe] " + "First pass vocab scan, #vocab = %d" % len(vocab)
		lg.PrintWriteLog(msg)


		# Step 2. Sort vocab, and doing min frequency cut-off

		if self.__nGramMinFreq > 1:
			for key in vocab.keys():
				freq = vocab[key]
				if freq < self.__nGramMinFreq:
					del vocab[key]

		msg = "[ProdRuleFe] " + \
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

		for wrtId in treeDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, nationality

			if classVal is None:
				continue

			treeList = treeDict[wrtId]
			for treeStr in treeList:
				# process each sentence

				attrList = []
				attrList.append('%d %s' % (0, classVal)) # Add class id first

				fes = self.__processSingleInstance(treeStr) # features from this tree

				attrUnsort = set() # Nominal feature!!!
				
				for fe in fes:
					if not attrIdx.has_key(fe):
						continue

					idx = attrIdx[fe] + attrIdxOffset
					attrUnsort.add(idx)
				
				if len(attrUnsort) <= 0: # TODO maybe reserve empty instace for combination
					continue
				
				# Sort the attribute list, as required for Sparse Data format in Weka
				attrSort = list(attrUnsort)
				attrSort.sort()
				
				# Write up atrribute list
				for idx in attrSort:
					attrList.append('%d %d' % (idx, 1))  # 1, means 'norminal'

				# Final step, adding to feautreList to return
				featureList.append(attrList)

		return (classSet, sortedVocab, featureList)

def main_test():

	td = SenTreeData.GetInstance()
	#td = SenTreeData.GetInstance('/home/xj229/data/test_1000line.tree')
	treeDict = td.GetTreeDict()

	nfe = ProdRuleExtractor()
	(clsSet, attrList, feList) = nfe.ExtractFeatureOnCorpus(treeDict)

	arffPath = '/home/xj229/test/prodRule_bog.arff'
	nfe.OutputArffFile(arffPath, clsSet, attrList, feList)

	libsvmPath = arffPath + ".libsvm"
	nfe.ConvertArff2Libsvm(arffPath, libsvmPath)
	
if __name__ == '__main__':
	import cProfile
	cProfile.run('main_test()')

