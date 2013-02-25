'''
Created on 23 Feb 2013

@author: xj229
'''

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Util'))
sys.path.append(os.path.dirname(__file__))

from LibSvmSh import *
from WekaSh import *

def RunNatClassifyig():

	testSet = [ \
						 "7nat_lvl123_6000each.bog_M10_L_STM", \
						 "7nat_lvl123_6000each.bog_M5_L", \
						 "7nat_lvl123_6000each.bog_M5_L_STM_ALPHANUM", \
						 "7nat_lvl123_6000each.bog_M5_L_STM", \
						 "7nat_lvl123_6000each.bog_M5_STM" \
						]

	testSet = ["7nat_lvl123_6000each.bog_M5_L_STM_RMSTP"]
	testFolder = "/home/xj229/data/"
	
	lg = Log()

	for ts in testSet:
		testSetFullName = testFolder + ts

#		# LibSVM
#		msg = "Start LibSVM evaluation: " + testSetFullName
#		print(msg)
#		lg.WriteLog(msg)
#		pfm = Perfmon()
#		pfm.Start()
#		lss = LibSvmSh()
#		lss.RunEval(testSetFullName + '.libsvm')
#		pfm.Stop()
#		msg = pfm.GetSummary()
#		print(msg)
#		lg.WriteLog(msg)
#
#		continue
		
		# Weka
		
		msg = "Start Weka evaluation: " + testSetFullName
		print(msg)
		lg.WriteLog(msg)
		pfm = Perfmon()
		pfm.Start()
		ws = WekaSh()
		ws.RunEval(testSetFullName + '.arff')
		pfm.Stop()
		msg = pfm.GetSummary()
		print(msg)
		lg.WriteLog(msg)

if __name__ == '__main__':
	RunNatClassifyig()
