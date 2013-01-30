## Read sentence data: senssel:
import re

class SensData:
	def __init__(self):
		self.__sens = {}
		self.__fileName = ""

		patPunct = r"\,|\"|\?|\!|\&|\$|\\|/|\(|\)|:"
		self.__rexPunct = re.compile(patPunct)

		self.__wrtIdx = 0

	def ResetWritingIter(self):
		self.__wrtIdx = 1
	
	def GetNextWriting(self):
		if self.__wrtIdx >= len(self.__sens):
			return (None, None)
		else:
			rslt = self.__sens[self.__wrtIdx]
			curId = self.__wrtIdx

			self.__wrtIdx += 1
			while not self.__sens.has_key(self.__wrtIdx):
				if self.__wrtIdx >= len(self.__sens):
					break
				self.__wrtIdx += 1
				
			return (curId, rslt)
		

	def ProcSen(self, sen):
		
		sen = sen.strip()
		if not sen[-1].isalpha():
			sen = sen[0:-1]
		sen = self.__rexPunct.sub(" ", sen)

		return sen

	def Read(self, senFn):
		self.__fileName = senFn
		fr = open(self.__fileName, 'r')
		lines = fr.readlines()
		fr.close()

		for line in lines:
			#print line
			sp = line.split('\t')

			tags = sp[0].split(':')
			sen = self.ProcSen(sp[1])
		
			wrtId = int(tags[0])
			senId = int(tags[1])
			#print("%d:%d" % (wrtId, senId))
	
			senList = []
			if self.__sens.has_key(wrtId):
				senList = self.__sens[wrtId]
			
			senList.append(sen)
			self.__sens[wrtId] = senList
			#print("%d, %d ==> %d" % (len(senList), senId, len(self.__sens)))
			if(0):#len(senList) != senId):
				print("%d, %d ==> %d" % (len(senList), senId, len(self.__sens)))
				

		print("Sentence Data load complted! #Sentences=%d" % len(self.__sens))

	def GetAllSentences(self):
		rslt = []
		for senList in self.__sens.values():
			rslt.extend(senList)

		return rslt

	def GetAllSentencesWrtId(self):
		rslt = []
		for wrtId in self.__sens.keys():
			for sen in self.__sens[wrtId]:
				rslt.append((wrtId, sen))

		return rslt