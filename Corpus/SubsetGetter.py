'''
Created on 2013-2-7

@author: Xiao
'''


import sys,os
sys.path.append('../')
sys.path.append('./')

from Corpus.WritingData import *
from Corpus.SensData import *
from Corpus.SubSetCriteria import *
from Corpus.SenTreeData import *
from Corpus.DependData import *
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


		self.__criSet = SubSetCriteria()
		self.__criSet.SetWritingDataObj(self.WdObj)

	def AddCriteria(self, colStr, criVal):
		self.__criSet.AddCriteria(colStr, criVal)

	def GetSummaryCriStr(self):
		"""
		Get the summary of current criteria set
		"""
		return self.__criSet.GetSummaryStr()

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
		
		lg = Log()
		allWrt = 0

		for wid in widList:
			wid = int(wid)

			if not dataDict.has_key(wid):
				continue

			data = dataDict[wid]
			fw.write('%s\n' % '\t'.join(data))
			allWrt += 1

				
		fw.flush()
		fw.close()

		lg.WriteLog("%d sentences has been wrote to %s" % (allWrt, outputFn))

		
	def __outputDependFormat(self, widList, outputFn):
		"""
		Output the subset in tree data format
		"""

		fw = open(outputFn, 'w')
		
		if self.SdObj is None:
			cf = ConfigFile()
			self.SdObj = SensData()
			self.SdObj.Read(cf.GetConfig("SENSDATA"))

		dd = DependData.GetInstance()
		sensDataDict = dd.GetDict()
		print(len(sensDataDict.keys()))
		a = raw_input('pause..')

	
		lg = Log()
		allSens = 0
		missing = 0
		for wid in widList:
			wid = int(wid)
			if not sensDataDict.has_key(wid):
				#print("Key not found: %d" % wid)
				missing += 1
				continue

			senList = sensDataDict[wid]
			senId = 1
			for sen in senList:
				fw.write("%d:%d\t%s\n" % (wid, senId, sen))
				senId += 1
				allSens += 1

		fw.flush()
		fw.close()

		lg.PrintWriteLog("%d sentences has been wrote to %s." % (allSens, outputFn))
		lg.PrintWriteLog("%d writings missed!" % missing)

	def __outputTreeFormat(self, widList, outputFn):
		"""
		Output the subset in tree data format
		"""

		fw = open(outputFn, 'w')
		
		if self.SdObj is None:
			cf = ConfigFile()
			self.SdObj = SensData()
			self.SdObj.Read(cf.GetConfig("SENSDATA"))

		td = SenTreeData.GetInstance()
		sensDataDict = td.GetSensDict()
		print(len(sensDataDict.keys()))
		a = raw_input('pause..')

	
		lg = Log()
		allSens = 0
		missing = 0
		for wid in widList:
			wid = int(wid)
			if not sensDataDict.has_key(wid):
				#print("Key not found: %d" % wid)
				missing += 1
				continue

			senList = sensDataDict[wid]
			senId = 1
			for sen in senList:
				fw.write("%d:%d\t%s\n" % (wid, senId, sen))
				senId += 1
				allSens += 1

		fw.flush()
		fw.close()

		lg.PrintWriteLog("%d sentences has been wrote to %s." % (allSens, outputFn))
		lg.PrintWriteLog("%d writings missed!" % missing)

	def __outputSdFormat(self, widList, outputFn):
		"""
		Output the subset in sens data format
		"""

		fw = open(outputFn, 'w')
		
		if self.SdObj is None:
			cf = ConfigFile()
			self.SdObj = SensData()
			self.SdObj.Read(cf.GetConfig("SENSDATA"))

		sensDataDict = self.SdObj.GetSensDict()
		
		lg = Log()
		allSens = 0
		for wid in widList:
			wid = int(wid)
			if not sensDataDict.has_key(wid):
				continue

			senList = sensDataDict[wid]
			senId = 1
			for sen in senList:
				fw.write("%d:%d\t%s\n" % (wid, senId, sen))
				senId += 1
				allSens += 1

		fw.flush()
		fw.close()

		lg.WriteLog("%d sentences has been wrote to %s" % (allSens, outputFn))

	def OutputSubset(self, widList, outputPath):
		cf = ConfigFile()
		
		#outputPath = cf.GetConfig("SUBSETOUTPUT")
		outFormat = cf.GetConfig("SUBSETFORMAT")
		print("Will write %d wid to %s" % (len(widList),outputPath))
		if outFormat == "WRITINGDATA":
			self.__outputWdFormat(widList, outputPath)
		elif outFormat == "SENSDATA":
			self.__outputSdFormat(widList, outputPath)
		elif outFormat == "TREEDATA":
			self.__outputTreeFormat(widList, outputPath)
		elif outFormat == "DEPDDATA":
			self.__outputDependFormat(widList, outputPath)
		else:
			print("Wrong outFormat")
			assert(False)

	def ReadWidList(self, widListPath):
		"""
		Read wid list from file
		The file should contain a wid per line
		"""

		fr = open(widListPath, 'r')
		list = fr.readlines()
		fr.close()
		msgStr = "Read %d wid from file %s" % (len(list), widListPath)
		print(msgStr)
		lg = Log()
		lg.WriteLog(msgStr)
		return list

	def WriteWidList(self, widList, outPath):
		"""
		Output the given wid list to disk
		"""
		fw = open(outPath, 'w')
		
		i = 0
		for wid in widList:
			fw.write(str(wid) + "\n")
			i += 1
		print("%d wid wrote to file: %s" % (i, outPath))
		fw.close()


######################
# Global run
######################

def main_Get7natlvl123SubsetWid():
	cf = ConfigFile()
	lg = Log()

	for nat in ['cn','fr','de','mx','ru','br','it']:
		lg.WriteLog("\n\nProcessing " + nat)

		sg = SubsetGetter()
		sg.AddCriteria("Nationality", nat)
		sg.AddCriteria("LevelNo", 1)
		sg.AddCriteria("LevelNo", 2)
		sg.AddCriteria("LevelNo", 3)

		# Get list
		widList = sg.GetWidSet()

		# Write and log
		outPath = cf.GetConfig("DATAFOLDER") + "/%s_lvl123" % nat \
						  + ".widlist"

		lg.WriteLog(sg.GetSummaryCriStr())
		lg.WriteLog("Write %d wid to widlist %s" % (len(widList), outPath))
		sg.WriteWidList(widList, outPath)

def main_Combine7natlvl123SubsetWid():
	cf = ConfigFile()
	lg = Log()

	sg = SubsetGetter()

	widListAll = []
	#for nat in ['cn','fr','de','mx','ru','br','it']:
	#for nat in ['cn','br']:
	for nat in ['cn','br', 'ru']:
		lg.WriteLog("\n\nProcessing " + nat)

	
		widList = sg.ReadWidList(cf.GetConfig("DATAFOLDER") + \
										   "/%s_lvl123" % nat + ".widlist")
		#max 10000
		#maxCnt = 42000 # for 2 nat
		maxCnt = 15000	# for 3 nat
		if len(widList) >= maxCnt:
			widList = widList[0:maxCnt]
			
		widListAll.extend(widList)
	
	#outputPath = cf.GetConfig("DATAFOLDER") + "/2nat_lvl123_42K.sen"
	outputPath = cf.GetConfig("DATAFOLDER") + "/3nat_lvl123_15K.depd"
	#lg.WriteLog("Output 2 nat lvl 123 42000 each sensdata to " + outputPath)
	lg.WriteLog("Output 3 nat lvl 123 each treedata to " + outputPath)
	sg.OutputSubset(widListAll, outputPath)

def main_Get3NatLvl123():
	sg = SubsetGetter()


	widListAll = []
	for nat in ['cn','fr','de','mx','ru','br','it']:
		lg.WriteLog("\n\nProcessing " + nat)

#		cn -> 162256
#		br -> 71182
#		ru -> 63470
#		it -> 19304
#		de -> 17030
#		mx -> 15802
#		fr -> 14067
#		sa -> 7743
#		us -> 6712
#		jp -> 6027
	
		sg.AddCriteria("Nationality", nat)
		sg.AddCriteria("LevelNo", 1)
		sg.AddCriteria("LevelNo", 2)
		sg.AddCriteria("LevelNo", 3)

		#widList = 
		
		#max 10000
		maxCount = 100000
		if len(widList) >= maxCount:
			widList = widList[0:6000]
			
		widListAll.extend(widList)
	
	outputPath = cf.GetConfig("DATAFOLDER") + "/7nat_lvl123_6000each.sen"
	lg.WriteLog("Output 7 nat lvl 123 conbined sensdata to " + outputPath)
	sg.OutputSubset(widListAll, outputPath)
	


if __name__ == '__main__':
	#main_Get7natlvl123SubsetWid()
	main_Combine7natlvl123SubsetWid()

	
		
	pass
	#widList = sg.GetWidSet()
#	widList = sg.ReadWidList(r"d:\Dropbox\Working Proj\ACS Proj\AcsProj\data\widList.dat")
#	print(len(widList))
#	sg.OutputSubset(widList)
	

