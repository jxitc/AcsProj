# Stop words list
#

class Vocab:
	def __init__(self):
		self.__dict = {}
		self.__listPath = ""
	
	def Read(self,listPath):
		self.__listPath = listPath
		fr = open(self.__listPath, 'r')
		lines = fr.readlines()
		fr.close

		for line in lines:
			self.__dict[wrd] = 1

		print("Stoplist load completed! %d words loaded" % len(self.__dict))

	def IsStopWords(self, word):
		word = word.upper()
		if self.__dict.has_key(word.strip()):
			return True
		else:
			return False

	def GetFrequency(self, word):
		wrd = word.strip().upper()
		if self.__dict.has_key(wrd):
			return int(self.__dict[wrd])
		else:
			return -1

	
