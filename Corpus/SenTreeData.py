import sys
sys.path.append('..')

from SenTreeReader import *
from Util.ConfigFile import *

class SenTreeData:
	"""
	Sentence syntactic tree data
	"""

	__existingSenTreeObjs = {}

	@staticmethod
	def GetInstance(senTreeFilePath = ""):
		if senTreeFilePath == "":
			# Read from config
			cf = ConfigFile()
			senTreeFilePath = cf.GetConfig('TREEDATA')

		if SenTreeData.__existingSenTreeObjs.has_key(senTreeFilePath):
			# if already exists:
			return SenTreeData.__existingSenTreeObjs[senTreeFilePath]
		else:
			# initialize new
			newSenTreeData = SenTreeData()
			newSenTreeData.__read(senTreeFilePath)
			SenTreeData.__existingSenTreeObjs[senTreeFilePath] = newSenTreeData
			return newSenTreeData
	
	def __init__(self):
		self.__sens = {}
		self.__fileName = ""

	def __read(self, treeFn):
		print("Start reading TreeData: " + treeFn)
		self.__fileName = treeFn
		fr = open(self.__fileName, 'r')
		lines = fr.readlines()
		fr.close()

		allSens = 0
		for line in lines:
			sp = line.strip().split('\t')

			tags = sp[0].split(':')
			sen = sp[1]
		
			wrtId = int(tags[0])
			senId = int(tags[1])
	
			senList = []
			if self.__sens.has_key(wrtId):
				senList = self.__sens[wrtId]
			
			allSens += 1
			
			senList.append(sen)
			self.__sens[wrtId] = senList

			if(0):#len(senList) != senId):
				print("%d, %d ==> %d" % (len(senList), senId, len(self.__sens)))

		print("Sentence Data load complted! #Sentences=%d" % allSens)

	def GetSensDict(self):
			return self.__sens

		

def AddWidToTreeData():
	oldTreeDataPath = '/mnt/scratch/xj229/data/20120220_senssel_CJ.dat.pcjr'
	newTreeDataPath = '/home/xj229/data/20120220_senssel_CJ.tree'

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
	std = SenTreeData.GetInstance()
	dict = std.GetSensDict()
	print(dict.keys()[0:100])

if __name__ == '__main__':
	#AddWidToTreeData()
	test()
