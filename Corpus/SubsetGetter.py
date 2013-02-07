'''
Created on 2013-2-7

@author: Xiao
'''

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Weka'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Util'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Script'))
sys.path.append(os.path.dirname(__file__))


from Corpus.WritingData import *
from Corpus.SensData import *
from Corpus.SubSetCriteria import *
from Util.Log import *
from Util.ConfigFile import *

class SubsetGetter:
	"""
	This class will extract wId which meet the pre-defined criteria
	"""
	
	WdObj = None # writing data obj
	SdObj = None # sentence data obj

	def __init__(self):
		cf = ConfigFile()

		if self.WdObj is None:
			self.WdObj = WritingData()
			self.WdObj.Read(cf.GetConfig("WRITINGDATA"))

		if self.SdObj is None:
			self.SdObj = SensData()
			self.SdObj.Read(cf.GetConfig("SENSDATA"))

		self.__criSet = SubSetCriteria()
		self.__criSet.SetWritingDataObj(self.WdObj)

	def AddCriteria(self, colStr, criVal):
		self.__criSet.AddCriteria(colStr, criVal)

	def GetWidSet(self):
		"""
		Get list (python list) of wId which meets the criteria
		"""

		dataDict = self.WdObj.GetDictData()
		rsltList = []
		for wid in dataDict.keys():
			data = dataDict[wid]
			if self.__criSet.Test(data):
				rsltList.append(wid)

		return rsltList
	
	def GetIntersectionList(self, list1, list2):
		"""
		Get the intersection of two list
		"""
		
		set1 = set(list1)
		set2 = set(list2)

		interSet = set1 & set2
		return list(interSet)
		
	def GetUnionList(self, list1, list2):
		"""
		Get the union of two list
		"""
		
		set1 = set(list1)
		set2 = set(list2)

		interSet = set1 | set2

		return list(interSet)

	
	def __outputWdFormat(self, widList, outputFn):
		"""
		Output the subset in writing data format
		"""
		
		fw = open(outputFn, 'w')
		colStrList = [x[0] for x in self.WdObj.GetColNames()]
		fw.write("%s\n" % '\t'.join(colStrList))
	
		dataDict = self.WdObj.GetDictData()

		for wid in widList:
			wid = int(wid)
			if not dataDict.has_key(wid):
				continue
			data = dataDict[wid]
			fw.write('%s\n' % '\t'.join(data))

				
		fw.flush()
		fw.close()

		
	def __outputSdFormat(self, widList, outputFn):
		"""
		Output the subset in sens data format
		"""

		fw = open(outputFn, 'w')
		
		sensDataDict = self.SdObj.GetSensDict()

		for wid in widList:
			wid = int(wid)
			if not sensDataDict.has_key(wid):
				continue

			senList = sensDataDict[wid]
			senId = 1
			for sen in senList:
				fw.write("%d:%d\t%s\n" % (wid, senId, sen))
				senId += 1

		fw.flush()
		fw.close()

	def OutputSubset(self, widList):
		cf = ConfigFile()
		outputPath = cf.GetConfig("SUBSETOUTPUT")
		outFormat = cf.GetConfig("SUBSETFORMAT")
		
		if outFormat == "WRITINGDATA":
			self.__outputWdFormat(widList, outputPath)
		elif format == "SENSDATA":
			self.__outputSdFormat(widList, outputPath)

	def ReadWidList(self, widListPath):
		"""
		Read wid list from file
		The file should contain a wid per line
		"""

		fr = open(widListPath, 'r')
		list = fr.readlines()
		fr.close()
		return list

		


if __name__ == '__main__':
	sg = SubsetGetter()
	sg.AddCriteria("Nationality", 'cn')
	sg.AddCriteria("LevelNo", 7)
	sg.AddCriteria("LevelNo", 6)
	sg.AddCriteria("LevelNo", 8)
	
	#widList = sg.GetWidSet()
	widList = sg.ReadWidList(r"d:\Dropbox\Working Proj\ACS Proj\AcsProj\data\widList.dat")
	print(len(widList))
	sg.OutputSubset(widList)
	
