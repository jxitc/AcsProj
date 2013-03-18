import sys
sys.path.append('../')

import re

from Corpus.Vocab import *

from PorterStemmer import *
from ConfigFile import *

class Tokenizer:
	"""
	Tokenizer class
	"""

	__instance = None
	

	@staticmethod
	def GetInstance():
		if Tokenizer.__instance is None:
			Tokenizer.__instance = Tokenizer()
			print("Tokenzier instance initilized")

		return Tokenizer.__instance

	@staticmethod
	def Split(sen):
		tkz = Tokenizer.GetInstance()
		return tkz.__split(sen)

	@staticmethod
	def ProcessToken(tok, \
									 isToLower			= True, \
									 isUseStemmer		= True, \
									 isAlphaNumOnly = False, \
									 isRmStopWords	= False):
		"""
		Process token using given setting: 
		convert to lower? use stemmer? keep only alphanum chars?
		remove stop words?
		"""

		tkz = Tokenizer.GetInstance()
		return tkz.__processToken(tok, isToLower, isUseStemmer,\
															isAlphaNumOnly, isRmStopWords)

	def __init__(self):
		"""
		Constructor
		"""
		pat = r'["\.,:;?!\(\)\[\]\<\>{}' + r"']"
		self.__rexPunct = re.compile(pat)
		self.__rexSpace = re.compile(r'\s+')
		self.__repPunctStr = r' '

		cf = ConfigFile()
		self.__stopWordsVocab = Vocab()
		stopList = cf.GetConfig("STOPLIST")
		self.__stopWordsVocab.Read(stopList)

		self.__ptStm = PorterStemmer()



	def __processToken(self, tok, isToLower, isUseStemmer, \
										 isAlphaNumOnly, isRmStopWords):
		"""
		Process token, according to the configuration setting
		i.e. lower? stemmer? etc.
		"""

		tok = tok.strip()
		if tok == '':
			return None

		isAllNonASCII = True
		findPos = False
		findPercent = False
		
		lenTok = len(tok)
		for i in range(lenTok, 0, -1):
			idx = i - 1
			ch = tok[idx]
			ordVal = ord(ch)
			
			if ordVal < 128:
				isAllNonASCII = False

			replaceCh = ''
			doReplace = False
			if ordVal <= 32:
				# Special char! need to wipe out
				replaceCh = ''
				doReplace = True

			if ch == "'":
				replaceCh = "\'"
				doReplace = True

			if ch == '%':
				replaceCh = "_PERCENT_"
				doReplace = True

			# Doing replace
			if doReplace:
				tok = tok[:idx] + replaceCh + tok[idx + 1:]
			
		if isAllNonASCII:
			return None

		if isRmStopWords:
			if self.__stopWordsVocab.IsVocabWord(tok):
				#print("REMOVED: " + tok)
				return None

		if isToLower:
			tok = tok.lower()

		if isUseStemmer:
			tok = self.__ptStm.stem(tok, 0, len(tok) - 1)

		if isAlphaNumOnly:
			if not tok.isalnum():
				return None

		return tok


	def __isAllNonASCII(self, string):
		return all(ord(c) >= 128 for c in string)
		
	def __split(self, sen):
		"""
		Split given sentcen. Return a set of tokens
		"""

		# First, replace punctuation
		sen = self.__rexPunct.sub(self.__repPunctStr, sen)
		#print sen

		# Split
		sp = self.__rexSpace.split(sen)

		# Process contiguous spaces
		lenSp = len(sp)

		for i in range(lenSp, 0, -1):
			idx = i - 1
			c = sp[idx].strip()
			if c == '' or c == None:
				del sp[idx]

		return sp

def main():
	while(True):
		s = raw_input("Input:")
		print(Tokenizer.Split(s))
		
def main_testProcessTok():
	while(True):
		tok = raw_input("Input:")
		print(Tokenizer.ProcessToken(tok))


if __name__ == '__main__':
	main_testProcessTok()
