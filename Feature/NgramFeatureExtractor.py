import sys
sys.path.append('..')

from Util.Tokenizer import *
from Util.ConfigFile import *
from Util.Log import *
from Util.PorterStemmer import *

from Corpus.WritingData import *
from Corpus.SensData import *

from FeatureExtractorBase import *

class NgramFeatureExtractor(FeatureExtractorBase):
	"""
	Extract ngram feature
	"""

	Description = "NgramFeatureExtractor"

	def __init__(self):
		cf = ConfigFile()
		self.__ngramN = int(cf.GetConfig("NGRAMFE_N"))
		self.__lg = Log()
		self.__lg.PrintWriteLog("Ngram Feature Extractor initialized, n = %d" \
														 % self.__ngramN)

		# If use only exact the n n-gram, i.e. not back-off
		self.__useExactNgram = True

		# Ngram config setting
		if cf.GetConfig("NGRAMFE_STEMMER") == 'TRUE':
			self.__isUseStemmer = True
		else:
			self.__isUseStemmer = False

		if cf.GetConfig("NGRAMFE_LOWER") == 'TRUE':
			self.__isToLower = True
		else:
			self.__isToLower = False

		self.__nGramMinFreq = int(cf.GetConfig("NGRAMFE_MINFREQ"))

		self.__bogMinFreq = int(cf.GetConfig("BOG_MINFREQ"))

		# Porter's stemmer
		self.__ptStm = PorterStemmer()

		#super(NgramFeatureExtractor, self).__init__()

	def SetNgramN(self, n):
		self.__ngramN = n

	def __getNgramStr(self, listObjs):
		"""
		Concatenate all elements in list to a string
		"""
		l = list(listObjs)
		strJoin = '|'
		return strJoin.join([str(s) for s in l])

	def __extractNgramPairs(self, toks, n):
		"""
		Extract ngram pairs from input token list
		@param toks: token list
		@param n: n in Ngram
		"""

		numToks = len(toks)
		stopIdx = numToks - n
	
		rsltList = []

		for idx in range(stopIdx + 1):
			tok = toks[idx]
			newTuple = (tok, )
			
			nextIdx = idx
			for nGramOffset in range(n - 1):
				nextIdx += 1
				nextTok = toks[nextIdx]
				newTuple += (nextTok, )
			
			rsltList.append(self.__getNgramStr(newTuple))

		return rsltList # possibly empty list []
		
	def __extractSingleSentence(self, sen):
		"""
		Extract ngram feature for single sentence
		"""

		oriToks = Tokenizer.Split(sen) # TODO this will omit all punctuation!!

		toks = []
		# Process toks
		for tok in oriToks:
			tok = Tokenizer.ProcessToken(tok, isToLower		 = self.__isToLower,\
																				isUseStemmer = self.__isUseStemmer)
			if tok != None:
				toks.append(tok)
		
		dictNgram = {}
		for n in range(self.__ngramN, 0, -1): 
			"""
			Store all ngram, -2, -1, etc
			"""

			if self.__useExactNgram and n != self.__ngramN:
				continue

			newList = self.__extractNgramPairs(toks, n)
			dictNgram[n] = newList

		return dictNgram

	def ExtractFeature(self, sensDict):
		"""
		Extract Ngram feature from sentece list. Assume each element is a pure text
		sentence
		"""
		
		lg = Log()
		msg = "Start extract ngram feature! n = %d" % self.__ngramN
		print(msg)
		lg.WriteLog(msg)

		wd = WritingData.GetInstance()
		#sd = SensData.GetInstance()
		#sensDict = sd.GetSensDict()

		# First pass, scan the whole, building vocabulary first
		vocab = {}
		classSet = set()
		classColStr = "Nationality"
		numWrt = 0
		for wrtId in sensDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, i.e. nationality
			classVal = classVal.lower()
			classSet.add(classVal)
			
			numWrt += 1
			if numWrt % 500 == 0:
				print("Processing #writing = %d" % numWrt)

			sensList = sensDict[wrtId]
			for sen in sensList:
				ngramDict = self.__extractSingleSentence(sen).values()
				ngrams = []
				for ngramDictElem in ngramDict:
					ngrams.extend(ngramDictElem)
				
				for ngram in ngrams:
					# start adding to vocabulary
					
					if ngram == None or ngram == '':
						continue
				
					if vocab.has_key(ngram):
						vocab[ngram] += 1
					else:
						vocab[ngram] = 1

		msg = "[NGramFE] " + "First pass vocab scan, #vocab = %d" % len(vocab)
		lg.PrintWriteLog(msg)


		# impose min ngram frequency cut-off, to eliminate those ngram whose
		# frequency is lower than threshold
		if self.__nGramMinFreq > 1:
			for word in vocab.keys():
				freq = vocab[word]
				if freq < self.__nGramMinFreq:
					del vocab[word]

		msg = "[NGramFE] " + \
					"Applied minimum frequency cut-off (#attr) #vocab = %d" % len(vocab)
		print(msg)
		lg.WriteLog(msg)


		import operator
		sortedVocab = sorted(vocab.iteritems(), \
												 key = operator.itemgetter(1), \
												 reverse = True)
		
		attrIdx = {} # Index for attributes, for later looking-up
		idx = 0
		
		
	#	iVocab = 0
	#	
	#	while iVocab < len(sortedVocab):
	#		(word, freq) = sortedVocab[iVocab]
	#		sortedVocabp
		for (word, freq) in sortedVocab:
			attrIdx[word] = idx
			idx += 1

		# 2nd Pass
		# Start extracting feature
		attrIdxOffset = 1 # Because the first attribute is "CLASS_LABEL", \
											# so we need to add this offset
		nSen = 0
		featureList = []
		for wrtId in sensDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, nationality

			if classVal is None:
				continue

			for sen in sensDict[wrtId]:
				# process each sentence

				attrList = []
				attrList.append('%d %s' % (0, classVal)) # Add class id first

				ngramDict = self.__extractSingleSentence(sen).values()
				ngrams = []
				for ngramDictElem in ngramDict:
					ngrams.extend(ngramDictElem)

				attrUnsort = set()

				for ngram in ngrams:
					# TODO not clear!

					if ngram == None or ngram == '':
						continue
					
					if not attrIdx.has_key(ngram):
						continue
					
					idx = attrIdx[ngram] + attrIdxOffset
					attrUnsort.add(idx)
				
				if len(attrUnsort) <= 0:
					print("Extract 0 features for data: " + sen)
					featureList.append(attrList) # Only has one attr, i.e. the class id
					continue
				
				attrSort = list(attrUnsort)
				attrSort.sort()
				
				for idx in attrSort:
					attrList.append('%d %d' % (idx, 1)) 

				# Final step, adding to feautreList to return
				featureList.append(attrList)

		return (classSet, sortedVocab, featureList)

def main_test():

	sd = SensData.GetInstance()
	sensDict = sd.GetSensDict()

	nfe = NgramFeatureExtractor()
	nfe.SetNgramN(1)
	(clsSet, attrList, feList) = nfe.ExtractFeature(sensDict)

	arffPath = '/home/xj229/test/nfeout_1gram.arff'
	nfe.OutputArffFile(arffPath, clsSet, attrList, feList)

	libsvmPath = arffPath + ".libsvm"
	nfe.ConvertArff2Libsvm(arffPath, libsvmPath)
	
if __name__ == '__main__':
	import cProfile
	cProfile.run('main_test()')
