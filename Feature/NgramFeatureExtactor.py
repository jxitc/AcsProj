import sys
sys.path.append('.')
sys.path.append('..')

from Util.Tokenizer import *
from Util.ConfigFile import *
from Util.Log import *
from Util.PorterStemmer import *

from Corpus.WritingData import *
from Corpus.SensData import *

class NgramFeatureExtractor(FeatureExtractorBase):
	"""
	Extract ngram feature
	"""

	Description = "NgramFeatureExtractor"

	def __init__(self):
		cf = ConfigFile()
		self.__ngramN = cf.GetConfig("NGRAMFE_N")
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




		super(NgramFeatureExtractor, self).__init__()
		
	def __processToken(self, tok):
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
			tok = "'%sp" % tok.replace("%", r"\%")

		if self.__rmStopWords:
			if self.__stopWordsVocab.IsVocabWord(tok):
				#print("REMOVED: " + tok)
				return None

		if self.__isToLower:
			tok = tok.lower()

		if self.__isUseStemmer:
			tok = self.__ptStm.stem(tok, 0, len(tok) - 1)

		return tok

	def __getNgramStr(self, listObjs):
		"""
		Concatenate all elements in list to a string
		"""
		l = list(listObjs)
		strJoin = '\t'
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
			tok = self.__processToken(tok)
			if tok != None:
				toks.append(tok)
		
		dictNgram = {}
		for n in range(self.__ngramN, 1, -1): # Bog words is special one! so, n to 2
			"""
			Store all ngram, -2, -1, etc
			"""

			if self.__useExactNgram and n != self.__ngramN:
				continue

			newList = self.__extractNgramPairs(toks, n)
			dictNgram[n] = newList

		return dictNgram

	def ExtractFeature(self, sensList):
		"""
		Extract Ngram feature from sentece list. Assume each element is a pure text
		sentence
		"""
		
		lg = Log()
		msg = "Start extract ngram feature! n = %d" % self.__ngramN
		print(msg)
		lg.WriteLog(msg)

		wd = WritingData.GetInstance()
		sd = SensData.GetInstance()
		sensDict = sd.GetSensDict()

		# First pass, scan the whole, building vocabulary first
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
				ngrams = self.__extractSingleSentence(sen)
				
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


		# impose min word frequency cut-off
		if self.__minFreq > 1:
			for word in vocab.keys():
				freq = vocab[word]
				if freq < self.__minFreq:
					del vocab[word]

		msg = "[NGramFE] " + "Applied minimum frequency cut-off (#attr) #vocab = %d" % len(vocab)
		print(msg)
		lg.WriteLog(msg)


		import operator
		sortedVocab = sorted(vocab.iteritems(), key = operator.itemgetter(1), reverse = True)
		
		attrIdx = {} # Index for attributes, for later looking-up
		idx = 0
		for (word, freq) in sortedVocab:
			attrIdx[word] = idx
			idx += 1

		# 2nd Pass
		# Start extracting feature
		attrIdxOffset = 1 # because the first attribute is "CLASS_LABEL", so we need to add this offset
		nSen = 0
		featureList = []
		for wrtId in sensDict.keys():
			# wrtId (int)
			classVal = wd.GetValueByWid(wrtId, classColStr) # classId, i.e. nationality

			if classVal is None:
				continue

			for sen in sensDict[wrtId]:
				# process each sentence

				attrList = []
				attrList.append('%d %s' % (0, classVal)) # Add class id first

				ngrams = self.__extractSingleSentence(sen)

				attrUnsort = set()

				for tok in toks:
					tok = self.ProcessToken(tok)
					
					if not attrIdx.has_key(tok):
						continue
					
					idx = bogAttrIdx[tok] + attrIdxOffset
					attrUnsort.add(idx)
				
				if len(attrUnsort) <= 0:
					continue
				
				attrSort = list(attrUnsort)
				attrSort.sort()
				
				for idx in attrSort:
					attrList.append('%d %d' % (idx, 1)) 

				# Final step, adding to feautreList to return
				feautreList.append(attrList)

		return (classSet, sortedVocab, featureList)
