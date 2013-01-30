import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'CorpProc'))
sys.path.append(os.path.dirname(__file__))

from WritingData import *
from SensData import *
import re

from var import *

def TestWritingData():
	fn = HomeData + "/writing_all_shrinked.dat"
	wd = WritingData()
	wd.Read(fn)
	cols = wd.GetColNames()
	print cols

	d = wd.GetData(3002)
	print d

	print("%d == %d ?" % (len(cols), len(d)))
	val = wd.GetValue(d, 'Grade')
	print val

def TestSensData():
	fn = HomeData + "/senssel.dat"
	sd = SensData()
	sd.Read(fn)
	sens = sd.GetAllSentences()

	for i in range(len(sens)):
		print("%d.%s" % (i+1, sens[i]))
	
	
TestSensData()

# TestWritingData()
