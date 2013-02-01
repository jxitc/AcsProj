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
	
if __name__ == '__main__':
	GetStat()

	
	
	

