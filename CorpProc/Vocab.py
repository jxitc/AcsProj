# Vocabulary
#

class Vocab:
	def __init__(self):
		self.__dict = {}
		self.__vocabPath = ""
	
	def Read(self,vocabPath):
		self.__vocabPath = vocabPath
		fr = open(self.__vocabPath, 'r')
		lines = fr.readlines()
		fr.close

		for line in lines:
			sp = line.strip().split('\t')
			wrd = sp[0]
			frq = sp[1]
			self.__dict[wrd] = frq

		print("Vocab load completed! %d words loaded" % len(self.__dict))

	def IsVocabWord(self, word):
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

	
