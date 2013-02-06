'''
Created on 2013-2-1

@author: Xiao
'''

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Corpus'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Weka'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Util'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Script'))
sys.path.append(os.path.dirname(__file__))

print(sys.path)

from Corpus.WritingData import *

from Util.Log import *
from Util.ConfigFile import *

class SubSetCriteria:
	def __init__(self):
		self.__criSet = {} # i.e. ["levelNo":[1,2,3,4]; 
											 #			 "Nationality":['cn', 'fr'] ... etc.
											 #			]
		self.__wd = None
		self.__colName = {}

	def AddCriteria(self, colStr, criVal):
		valSet = []
		if self.__criSet.has_key(colStr):
			valSet = self.__criSet[colStr]
		valSet.append(criVal)
		self.__criSet = valSet
	
	
	def SetWritingDataObj(self, wdObj):
		self.__wd = wdObj
		self.__colName = self.__wd.GetDictColName()

	def GetSummaryStr(self):
		"""
		Get a string of description of current defined criteria
		"""

		rsltStr = ""
		for colCri in self.__criSet.keys():
			rsltStr += colCri + "\t["

			valSet = self.__criSet[colCri]
			if valSet == []:
				continue

			valStr = ""
			for v in valSet:
				valStr += "%s, " % v

			valStr = valStr.strip() # remove trailing space
			valStr = valStr[0:-1]		# remove last comma ','

			rsltStr += valStr + "]\n"

		return rsltStr
			


	def Test(self, data):
		"""
		Test if given data is accordance with the pre-defined
		crateira
		"""
		assert(self.__wd != None)
		assert(self.__criSet != {})

		for colCri in self.__criSet.keys():
			colStr = colCri
			criValSet = self.__criSet[colStr]
			colId = self.__colName[colStr]
			tgtVal = data[colId]

			# test if the data is equal to any of the
			# value in criValSet
			anyCri = False
			for val in criValSet:
				if val == tgtVal:
					anyCri = True
					break
	
			if anyCri == False: # none of the value satisfied the criteria
				return False

		return True

class SubsetGetter:
	"""
	This class will extract wId which meet the pre-defined criteria
	"""
	
	WdObj = None # writing data obj
	SdObj = None # sentence data obj

	def __init__(self):
		cf = ConfigFile()

		if WdObj is None:
			self.WdObj = WritingData()
			self.WdObj.Read(cf.GetConfig("WRITINGDATA"))

		if SdObj is None:
			self.SdObj = WritingData()
			self.SdObj.Read(cf.GetConfig("SENSDATA"))

		self.__criSet = SubSetCriteria()
		self.__criSet.SetWritingDataObj(self.WdObj)

	def AddCriteria(self, colStr, criVal):
		self.__criSet.__criSet.AddCriteria(colStr, criVal)

	def GetWidSet(self):
		"""
		Get list (python list) of wId which meets the criteria
		"""

		dataDict self.WdObj.GetDictData()
		rsltList = []
		for wid in dataDict.keys()
			data = dataDict[wid]
			if self.__criSet.Test(data)
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
		
		
	
	def __outputSdFormat(self, widList, outputFn):
		"""
		Output the subset in sens data format
		"""

		sensDataDict = self.SdObj.GetSensDict()

		for wid in widList:
			if not sensDataDict.has_key(wid):
				continue

			sens = wid.

	def OutputSubset(self, widList):

		


		
			
		
		
	

def GetStatStr(stat):
	rsltStr = ""
	for e in stat:
		rsltStr += "%s -> %d\n" % (e[0], e[1])

	return rsltStr.strip()

def GetStat():
	col1 = "Nationality"
	col2 = "LevelNo"
	wd = WritingData()
	cf = ConfigFile()
	wd.Read(cf.GetConfig("WRITINGDATA"))
	stat1 = wd.GetStat(col1)
	stat2 = wd.GetStat(col2)

	lg = Log()


	print("Print Nationality:")
	print(GetStatStr(stat1))
	lg.WriteLog(GetStatStr(stat1))
	
	print()

	print("Print LevelNo")
	print(GetStatStr(stat2))
	lg.WriteLog(GetStatStr(stat2))


# deprecated! TODO
def GetNatIdx(natList, natName):
	natName = natName.strip().lower()
	i = 0
	for i in range(len(natList)):
		if natList[i] == natName:
			return i

	return -1

def GetLvlIdx(lvlGroup, lvl):
	lvl = int(lvl)
	i = 0
	for i in range(len(lvlGroup)):
		minL = lvlGroup[i][0]
		maxL = lvlGroup[i][1]
		if lvl >= minL and lvl <= maxL:
			return i

	return -1

def GetSubsetIndex():
	natList = ['cn', 'br', 'ru', 'it', 'de', 'mx', 'fr']
	nNat = len(natList)

	#lvlGroup = [(1, 1), (2, 4), (5, 7), (8, 10), (11, 16)] 
	#lvlGroup = [(1, 3), (4, 6), (7, 9), (10, 12), (13, 16)]
	lvlGroup = [(1, 1), (2, 3), (4, 5), (6, 8), (9, 16)] 
	nLvlGroup = len(lvlGroup)

	maxDataNat = 14067 # max data per nation (since min = fr = 14067)
	#maxDataLvl = maxDataNat / nLvlGroup # about 2830
	maxDataLvlRatio = [1.0/4, 1.0/6, 1.0/8, 1.0/10, 1.0/12]
	
	sumRatio = 0.0 
	for r in maxDataLvlRatio:
		sumRatio += r
	
	portion = maxDataNat / sumRatio
	maxDataLvl = [0] * nLvlGroup
	import math
	for iLvl in range(nLvlGroup):
		maxDataLvl[iLvl] = math.ceil(portion \
											 * maxDataLvlRatio[iLvl])
	
	print(maxDataLvl)
	#return
	

	wd = WritingData()
	cf = ConfigFile()
	wd.Read(cf.GetConfig("WRITINGDATA"))
	
	colName = wd.GetDictColName()
	data = wd.GetDictData()


	# Initialize rsltWidList dictionary, contains wid of 
	# result subset
	rsltWidList = {}

	# statistics for existing number in a group						 
  # for each nation
	statLvl = {} 

	# statistics for exisiting data for each nation
	statNat = {}

	i = 0

	for n in natList:
		rsltWidList[n] = [] # initialize!
		statNat[n] = 0
		statLvl[n] = [0] * nLvlGroup

	idxWid = colName["WritingId"]
	idxNat = colName["Nationality"]
	idxLvl = colName["LevelNo"]

	nCnG4 = 0 # TODO
	# Start counting data!
	for d in data.values():
		wid = int(d[idxWid])
		nat = d[idxNat].lower().strip()
		lvl = d[idxLvl]
		lvlGroupId = GetLvlIdx(lvlGroup, lvl)
		
		if lvlGroupId == 4 and nat == "cn":
			nCnG4 += 1

		
			
		# if not in target nation list, Pass!
		if not statNat.has_key(nat):
			continue

		# if this nation already got enough data, Pass!
		nNatData = statNat[nat]
		if nNatData >= maxDataNat:
			continue

		# if this group already got enough data, Pass!
		nLvlData = statLvl[nat][lvlGroupId]
		if nLvlData >= maxDataLvl[lvlGroupId]:
			continue
		
		# OK! add to result set!
		rsltWidList[nat].append(wid)

		# Update statistics!
		statNat[nat] += 1
		statLvl[nat][lvlGroupId] += 1
	

	# Finished! print out result
	rsltStr = "Statistics for subset division:\n"

	for n in natList:
		rsltStr += "\nStat. [%s]:\n" % n
		lvlList = statLvl[n]
		lvlId = 0
		for l in lvlList:
			rsltStr += "\tGroup %d -> %d\n" % (lvlId, l)
			lvlId += 1

	# print writing per group
	rsltStr += "\nNumber of writings per group:\n"
	for i in range(nLvlGroup):
		lvlgrp = lvlGroup[i]
		lMin = lvlgrp[0]
		lMax = lvlgrp[1]
		lNumData = maxDataLvl[i]
		rsltStr += "\tGroup[%d] lvl%d -lvl%d:\t%d\n" % \
							 (i, lMin, lMax, lNumData)

	lg = Log()
	lg.WriteLog(rsltStr)
	print(rsltStr)
	
	print nCnG4
	
	return (natList, lvlGroup, rsltWidList)


	
	
if __name__ == '__main__':
	# GetStat()
	GetSubsetIndex()

#	lvlGroup = [(1, 3), (4, 6), (7, 9), (10, 12), (13, 16)] 
#	for i in range(16):
#		print(GetLvlIdx(lvlGroup, i+1))

	
	
	

