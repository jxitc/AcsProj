import sys,os
sys.path.append('../')
sys.path.append('./')

from Util.Log import *

class CvEvaluator:
	"""
	Evaluation the cross validation result
	"""

	def __dictAddOne(self, dict, key):
		"""
		Add one to certain key. If doesn't previous contain this key,
		add new key!
		"""
		if dict.has_key(key):
			dict[key] += 1
		else:
			dict[key] = 1
		
	def __compareLabels(self, goldLbl, sysLbl):
		"""
		Get the evaluation result between golden standard (goldLbl), and 
		the system output (sysLbl)
		"""
	
		#print(goldLbl[0:10])
		#print(sysLbl[0:10])
		assert(len(goldLbl) == len(sysLbl))

		uniqueGold = set(goldLbl)
		uniqueSys = set(sysLbl)
		allLable = uniqueSys.union(uniqueGold)
		nLable = len(allLable)
		
		# statistics dictionary for each class
		dictTp = {}
		dictFp = {}
		dictFn = {}
		dictTn = {}

		statTotal = 0
		statCorrect = 0
		for i in range(len(goldLbl)):
			lGold = goldLbl[i]
			lSys = sysLbl[i]

			if len(lSys) != 1:
				print lSys
				return # TODO

			# Calc accuracy
			statTotal += 1
			if lGold == lSys:
				statCorrect += 1
				
				# TP!
				self.__dictAddOne(dictTp, lGold)
				
				# TN!
				for lbl in allLable:
					if lbl != lGold:
						self.__dictAddOne(dictTn, lbl)

			else:

				# false negative, missing result
				self.__dictAddOne(dictFn, lGold)

				# false positive, unexpected result
				self.__dictAddOne(dictFp, lSys)

				for lbl in allLable:
					if lbl != lGold and lbl != lSys:
						self.__dictAddOne(dictTn, lbl)
				
			
		lg = Log()	
		dictPrecision = {}
		dictRecall = {}
		dictF1 = {}
		totalF1 = 0

		for lbl in allLable:
			if not dictTp.has_key(lbl):
				dictTp[lbl] = 0

			if not dictFp.has_key(lbl):
				dictFp[lbl] = 0

			if not dictFn.has_key(lbl):
				dictFn[lbl] = 0

			if not dictTn.has_key(lbl):
				dictTn[lbl] = 0

			 
			# Do P/R/F calculation
			tp = dictTp[lbl]
			fp = dictFp[lbl]
			fn = dictFn[lbl]
			tn = dictTn[lbl]

			totalNum = tp + fp + fn + tn
			precision = float(tp) / float(tp + fp)
			recall = float(tp) / float(tp + fn)
			f1 = 2 * precision * recall / (precision + recall)

			dictPrecision[lbl] = precision
			dictRecall[lbl] = recall
			dictF1[lbl] = f1
			totalF1 += f1

			# Output result
			msg = "lable [%s]: tp=%d, fp=%d, fn=%d, tn=%d, total=%d\n" \
						% (lbl, tp, fp, fn,tn, totalNum)
			msg += "P=%.2f, R=%.2f, F1=%.2f\n" % (precision, recall, f1)


			lg.PrintWriteLog(msg)

		# output all result:
		averageF1 = float(totalF1) / float(nLable)

		msg = "Average F1 = %.2f\n" % averageF1
		msg += "Accuracy = %d/%d = %f" % \
		       (statCorrect, statTotal, float(statCorrect) / float(statTotal)) 

		lg.PrintWriteLog(msg)

		return (dictPrecision, dictRecall, dictF1)
		

	def __evalLibSvm(self, testFile, predictFile):
		# read test label

		lg = Log()
		lg.PrintWriteLog("Evaluate on libsvm result:\nGold: %s\nSys:%s" \
										 % (testFile, predictFile))

		fr = open(testFile, 'r')
		dataLines = fr.readlines()
		fr.close()

		#x = dataLines[0]
		#sp = x.split(' ')
		#print sp
		#print sp[0][0]
		#return 
		
		testLabel = [d.split(' ')[0][0] for d in dataLines]

		# read predict label
		fr = open(predictFile, 'r')
		dataLines = fr.readlines()
		fr.close()
		predictlabel = [d.strip() for d in dataLines]

		# The following is just for testing 
		#testLabel =		 ['0','1','2','2','1','0','1','2','0','1']
		#predictlabel = ['2','1','2','0','1','0','2','2','1','0']

		(dictPrecision, dictRecall, dictF1) = \
				self.__compareLabels(testLabel, predictlabel)

		return (dictPrecision, dictRecall, dictF1)
	
	def __evalWekaOutput(self, wekaOutputLog):
		strCm = '=== Confusion Matrix ==='
		
		import re

		found = False
		fr = open(wekaOutputLog, 'r')
		line = fr.readline()
		# TODO
		while line:
			line = line.strip()
			
			line = fr.readline()

	def Evaluate(self, testFile, predictFile):
		(fFullName, fExt) = os.path.splitext(testFile)
		(dictPrecision, dictRecall, dictF1) = (None, None, None)
		if fExt == '.libsvm' or \
			 fExt == '.svm' or \
			 fExt == '.t':
				 
			(dictPrecision, dictRecall, dictF1) = \
					self.__evalLibSvm(testFile, predictFile)

		return (dictPrecision, dictRecall, dictF1)

def main():
	cvFolder = '/home/xj229/data/3nat_lvl123_15K.bog_M10_L_STM_CV4'
	testFile = cvFolder + '/fold1_tst.libsvm'
	predictFile = testFile + ".output"

	ce = CvEvaluator()
	ce.Evaluate(testFile, predictFile)

	
if __name__ == '__main__':
	main()
	
