import sys,os
sys.path.append('../')
sys.path.append('./')

from Util.Log import *
from Util.ConfigFile import *

class CvSplitter:
	"""
	Cross validation splitter
	"""

	def __splitIds(self, cids, nFold):
		"""
		Given a list of classId, split to nFold, result is the 
		index in original cids list
		"""
		freqDict = {}
		cDicts = {} # diction of class dictions
		idx = 0
		for l in cids:
			l = l.strip()
			if freqDict.has_key(l):
				freqDict[l] += 1
			else:
				freqDict[l] = 1

			cList = []
			if cDicts.has_key(l):
				cList = cDicts[l]
			else:
				cDicts[l] = cList
			
			cList.append(idx)
			idx += 1

		clsList = freqDict.keys()
		
		# finished first pass scan
		nPerClass = {}
		idxPerClass = {}
		for cls in clsList:
			nPerClass[cls] = float(freqDict[cls]) / float(nFold)
			idxPerClass[cls] = 0
			print("%s -> %d (%f)" % (cls, len(cDicts[cls]), nPerClass[cls]))

		print(" ")

		# start splitting
		rsltFoldIdxs = [] 
		for i in range(nFold):
			idPerFold = []
			
			for cls in clsList:
				nLimits = nPerClass[cls]
				cList = cDicts[cls]

				start = idxPerClass[cls]
				end = start + int(nLimits)
				if end > len(cList):
					end = len(cList)
				idPerFold.extend(cList[start:end])
				idxPerClass[cls] = end

				#for i in range(int(nLimits)):
				#	idxCls = idxPerClass[cls]
				#	if idxCls >= len(cList):
				#		print("!!!!!!!!!1idxCls >= len(cList):")
				#		break
				#	idPerFold.append(cList[idxCls]) 
				#	#idPerFold.append(cls)
				#	idxPerClass[cls] += 1
			
			rsltFoldIdxs.append(idPerFold)

		# put rest ids to the last fold result
		lastFoldRslt = rsltFoldIdxs[-1]
		for cls in clsList:
			cList = cDicts[cls]
			idxCls = idxPerClass[cls]
			start = idxCls
			end = len(cList)
			if start < end:
				print('(%d, %d)' % (start,end))
				lastFoldRslt.extend(cList[start:end])


			#while idxCls < len(cList):
			#	lastFoldRslt.append(cList[idxCls])
			#	idxCls += 1
			#idxPerClass[cls] = idxCls
		rsltFoldIdxs[-1] = lastFoldRslt

		# Verify:
		msg = "nFold Splitting! Original data set size: %d\n" % len(cids)
		msg += "New nFold result size:\n"
		totalNum = 0
		for i in range(nFold):
			msg += "\tFold %d -> %d\n" % (i, len(rsltFoldIdxs[i]))
			totalNum += len(rsltFoldIdxs[i])
		msg += "Total = %d\n" % totalNum

		lg = Log()
		lg.PrintWriteLog(msg)

		return rsltFoldIdxs

	def __makeDir(self, dirName):
		if os.path.exists(dirName):
			return

		# Make dir
		os.makedirs(dirName)
	
	
	def __writeLibSvmFile(self, outputPath, dataLines):
		"""
		Write data lines to outputPath
		LibSVM format
		"""
		fw = open(outputPath, 'w')
		for line in dataLines:
			fw.write(line.strip() + '\n')
		fw.flush()
		fw.close()

	def __splitLibSvmFile(self, libsvmFile, nFold):
		"""
		Split libsvm format:
			4.0 2232:1.0 2243:1.0 2777:1.0 2807:1.0
			4.0 1659:1.0 2031:1.0 2363:1.0 3366:1.0 3604:1.0
		"""
		
		fr = open(libsvmFile, 'r')
		dataList = fr.readlines() # TODO remember to .strip()! 
		fr.close()

		cids = [data.split(' ')[0] for data in dataList]

		nFoldIds = self.__splitIds(cids, nFold)

		
		(nameFolder, nameFile) = os.path.split(libsvmFile)
		(fName, fExt) = os.path.splitext(nameFile)
		cvFolder = os.path.join(nameFolder, '%s_CV%d' % (fName, nFold))
		self.__makeDir(cvFolder)

		lg = Log()

		for i in range(nFold):
			# Output test
			fnTst = os.path.join(cvFolder, 'fold%d_tst%s' % (i, fExt))
			outputData = [dataList[idx] for idx in nFoldIds[i]]
			self.__writeLibSvmFile(fnTst, outputData)
			msg = "Fold %s test, %d data, output to %s" % (i, len(outputData), fnTst)
			lg.PrintWriteLog(msg)
			
			# Output others as train
			fnTrn = os.path.join(cvFolder, 'fold%d_trn%s' % (i, fExt))
			outputData = []
			for j in range(nFold):
				if j == i:
					continue
				jData = [dataList[idx] for idx in nFoldIds[j]]
				outputData.extend(jData)
			self.__writeLibSvmFile(fnTrn, outputData)
			msg = "Fold %s train, %d data, output to %s" % (i, len(outputData), fnTst)
			lg.PrintWriteLog(msg)
		

	def Split(self, oriFileName, nFold):
		"""
		Split the input file
		"""
		(fName, fExt) = os.path.splitext(oriFileName)
		if fExt == ".libsvm" or \
			 fExt == ".t" or \
			 fExt == ".svm":
			self.__splitLibSvmFile(oriFileName, nFold)
		else:
			print("Current do not support this format: " + fExt)
		

def main():
	cs = CvSplitter()
	fn = '/home/xj229/data/3nat_lvl123_15K.bog_M10_L_STM.libsvm'
	cs.Split(fn, 4)

if __name__ == '__main__':
	main()
