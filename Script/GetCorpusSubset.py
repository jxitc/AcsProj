'''
Created on 2013-2-1

@author: Xiao
'''

import sys,os
sys.path.append('../')
sys.path.append('./')

from Corpus.WritingData import *

from Util.Log import *
from Util.ConfigFile import *


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
	(natList, lvlGroup, rsltWidList) = GetSubsetIndex()
	cf = ConfigFile()
	fn = cf.GetConfig("DATAFOLDER") + "/widList.dat"
	fw = open(fn, 'w')
	
	widList= []
	for nat in rsltWidList.keys():
		widList.extend(rsltWidList[nat])
	
	for wid in widList:
		fw.write(str(wid) + "\n")
	
	fw.flush()
	fw.close()
	
		

#	lvlGroup = [(1, 3), (4, 6), (7, 9), (10, 12), (13, 16)] 
#	for i in range(16):
#		print(GetLvlIdx(lvlGroup, i+1))

	
	
	

