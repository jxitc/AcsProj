import sys,os
sys.path.append('../')
sys.path.append('./')

class CvEvaluator:
	"""
	Evaluation the cross validation result
	"""
	
	def __compareLabels(self, goldLbl, sysLbl):
		"""
		Get the evaluation result between golden standard (goldLbl), and 
		the system output (sysLbl)
		"""
	
		print(goldLbl[0:10])
		print(sysLbl[0:10])
		assert(len(goldLbl) == len(sysLbl))

		statTotal = 0
		statCorrect = 0
		for i in range(len(goldLbl)):
			lGold = goldLbl[i]
			lSys = sysLbl[i]

			if len(lSys) != 1:
				print lSys
				return 

			statTotal += 1
			if lGold == lSys:
				statCorrect += 1

		print("Accuracy = %d/%d = %f" % \
					(statCorrect, statTotal, float(statCorrect) / float(statTotal)) \
				 )

	
	def __evalLibSvm(self, testFile, predictFile):
		# read test label
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

		self.__compareLabels(testLabel, predictlabel)

	def Evaluate(self, testFile, predictFile):
		(fFullName, fExt) = os.path.splitext(testFile)
		if fExt == '.libsvm' or \
			 fExt == '.svm' or \
			 fExt == '.t':
			self.__evalLibSvm(testFile, predictFile)

		
		
		
def main():
	cvFolder = '/home/xj229/data/3nat_lvl123_15K.bog_M10_L_STM_CV4'
	testFile = cvFolder + '/fold1_tst.libsvm'
	predictFile = testFile + ".output"

	ce = CvEvaluator()
	ce.Evaluate(testFile, predictFile)

	
if __name__ == '__main__':
	main()
	
