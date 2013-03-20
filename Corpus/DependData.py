import sys
sys.path.append('..')

import re

from Util.ConfigFile import *

class DependData:
	"""
	Sentence syntactic tree data
	"""

	__existingDependObjs = {}

	@staticmethod
	def GetInstance(filePath = ""):
		if filePath == "":
			# Read from config
			cf = ConfigFile()
			filePath = cf.GetConfig('DEPDDATA')

		print("GetInstance() DependData path = " + filePath)

		if DependData.__existingDependObjs.has_key(filePath):
			# if already exists:
			print("Already Exists!")
			return DependData.__existingDependObjs[filePath]
		else:
			# initialize new
			print("Initialize New!")
			newDependData = DependData()
			newDependData.__read(filePath)
			DependData.__existingDependObjs[filePath] = newDependData
			return newDependData
	
	def __init__(self):
		self.__depends = {}
		self.__fileName = ""

		pat = r'(?P<DEPNAME>[^\(\)]+)\(' \
					 '(?P<DEP1>[^\s]+)\-(?P<IDX1>\d{1,2}), ' \
					 '(?P<DEP2>[^\s]+)\-(?P<IDX2>\d{1,2})' \
					 '\)'
		print(pat)
		self.__rexDep = re.compile(pat)


	def __read(self, fileName):
		print("Start reading DependData: " + fileName)
		self.__fileName = fileName
		fr = open(self.__fileName, 'r')
		lines = fr.readlines()
		fr.close()

		allSens = 0
		for line in lines:
			sp = line.strip().split('\t')

			tags = sp[0].split(':')
			deps = '\t'.join(sp[1:])
		
			wrtId = int(tags[0])
			senId = int(tags[1])
	
			senList = []
			if self.__depends.has_key(wrtId):
				senList = self.__depends[wrtId]
			
			allSens += 1
			
			senList.append(deps)
			self.__depends[wrtId] = senList

			if(0):#len(senList) != senId):
				print("%d, %d ==> %d" % (len(senList), senId, len(self.__depends)))

		print("Sentence Data load complted! #Sentences=%d" % allSens)

	def GetDict(self):
			return self.__depends

	def SplitDenpStr(self, sen):
		"""
		Split the dependency sentence, and return a list of 
		single dependency string
		"""

		sp = sen.strip().split('\t')
		return [d.strip() for d in sp]

	def GetDependName(self, depStr):
		"""
		Return only the dependancy name
		i.e. 'nsubj', 'poss' etc from 'advmod(,-5, Also-1)'
		"""
		
		idx = 0
		lenStr = len(depStr)
		depName = ""
		while idx < lenStr:
			ch = depStr[idx]
			if ch == '(':
				break
			else:
				depName += ch

			idx += 1

		return depName
		
	def ParseDependamcy(self, depStr):
		"""
		Parse a dependency string
		i.e. det(bottle-2, Each-1)
		"""
		# Using self.__rexDep to parse and match the dependency string
		return None


def AddWidToDependData():
	oldTreeDataPath = '/mnt/scratch/xj229/data/20120220_senssel_CJ.dat.pcjr.d2'
	newTreeDataPath = '/home/xj229/data/20120220_senssel.depd'

	sensData = '/mnt/scratch/xj229/data/20120220_senssel.dat'

	frSens = open(sensData, 'r')
	frOldTree = open(oldTreeDataPath, 'r')
	fwNewTree = open(newTreeDataPath, 'w')

	lineSens = frSens.readline()
	lineOldTree = frOldTree.readline()
	
	nLine = 0
	while lineSens:
		assert(lineOldTree != None and lineOldTree != '')
		sp = lineSens.strip().split('\t')
		senId = sp[0]
		fwNewTree.write(senId + '\t' + lineOldTree)
		lineSens = frSens.readline()
		lineOldTree = frOldTree.readline()

		nLine += 1
		if nLine % 1000 == 0:
			print nLine

	
	print("DONE")

def test():
	std = DependData.GetInstance()
	dict = std.GetSensDict()
	

if __name__ == '__main__':
	test()
	#AddWidToDependData()
