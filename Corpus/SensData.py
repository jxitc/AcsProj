## Read sentence data: senssel:
# a
import sys
sys.path.append('.')
sys.path.append('..')

import re
from Util.ConfigFile import *

class SensData:
	
	__instance = None

	@staticmethod
	def GetInstace():
		if SensData.__instance is None:
			cf = ConfigFile()
			sdPath = cf.GetConfig("SENSDATA")
			SensData.__instance = SensData()
			SensData.__instance.Read(sdPath)
			print("SensData instance initilized!")

		return SensData.__instance

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
		print("Start reading SensData: " + senFn)
		self.__fileName = senFn
		fr = open(self.__fileName, 'r')
		lines = fr.readlines()
		fr.close()
		
		allSens = 0

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
			
			allSens += 1
			
			senList.append(sen)
			self.__sens[wrtId] = senList
			#print("%d, %d ==> %d" % (len(senList), senId, len(self.__sens)))
			if(0):#len(senList) != senId):
				print("%d, %d ==> %d" % (len(senList), senId, len(self.__sens)))
				

		print("Sentence Data load complted! #Sentences=%d" % allSens)

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

	def GetSensDict(self):
		# Format:
		# {wrtId(int) : [sentens_list]}
		return self.__sens

def main():
	s1 = SensData.GetInstace()
	s2 = SensData.GetInstace()
	
	print("============")

	print s1
	print s2

	print(id(s1))
	print(id(s2))
	
if __name__ == '__main__':
	main()

