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

#	testSet = [ \
#						 "7nat_lvl123_6000each.bog_M10_L_STM", \
#						 "7nat_lvl123_6000each.bog_M5_L", \
#						 "7nat_lvl123_6000each.bog_M5_L_STM_ALPHANUM", \
#						 "7nat_lvl123_6000each.bog_M5_L_STM", \
#						 "7nat_lvl123_6000each.bog_M5_STM" \
#						]

	cfgStrList = ['M5_L_STM', \
								'M10_L_STM', \
								'M5_STM', \
								'M5_L', \
								'M5_L_STM_ALPHANUM', \
								'M5_L_STM_RMSTP']

	testSet = []
	testFolder = "/home/xj229/data/"
	
	if True:
		baseStr = testFolder + "7nat_lvl123_6000each.bog_"
	else:
		baseStr = testFolder + "3nat_lvl123_15K.bog_"

	lg = Log()

	doSvm = False
	doWeka = True
	
	for cfg in cfgStrList:
		#testSet.append("3nat_lvl123_15K.bog_" + cfg)
		testSet.append(baseStr + cfg)
			
		testSetFullName = baseStr + cfg
		
		
		if doSvm:
			# LibSVM
			msg = "Start LibSVM evaluation: " + testSetFullName
			print(msg)
			lg.WriteLog(msg)
			pfm = Perfmon()
			pfm.Start()
			lss = LibSvmSh()
			lss.RunEval(testSetFullName + '.libsvm')
			pfm.Stop()
			msg = pfm.GetSummary()
			print(msg)
			lg.WriteLog(msg)

		if doWeka:
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
