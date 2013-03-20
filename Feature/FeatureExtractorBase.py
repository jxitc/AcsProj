# Base class definition for Feature Extractor

import sys
sys.path.append('../')

from Weka.ArffBuilder import *
from Util.Log import *
from Script.WekaSh import *

class FeatureExtractorBase:
	"""
	Providing unified feature extraction interface
	"""

	Description = "FeatureExtractorBase"

	@staticmethod
	def ConvertArff2Libsvm(iArffPath, oLibsvmPath):
		"""
		Call the Weka Libsvm saver command to convert the arff file to
		libsvm path
		"""
		lg = Log()
		lg.PrintWriteLog("Start converting from ARFF to LIBSVM format:"\
										 "\nfrom: %s\nto: %s" % (iArffPath, oLibsvmPath))
		ws = WekaSh()
		ws.LibSVMSaver(iArffPath, oLibsvmPath)

	def ConcateTwoFeatureType(self, classLabelSet1, classLabelSet2, \
														attrList1, attrList2, \
														dataFeatureList1, dataFeatureList2):
		"""
		Concatenate two types of feature directly
		"""

		# Step 0, concatenate two classLabel
		concClassLable = classLabelSet1.union(classLabelSet2)

		# Step 1, concatenate attribute list
		# Noted that the attr list does not contain the first attr (class attr)
		# Note that there are might be some duplicated words!!!
		numAttrList1 = len(attrList1)
		numAttrList2 = len(attrList2)

		# first establish a hash table for all attr name in attrList1:
		attr1NameDict = {}
		for (attrName, x) in attrList1:
			attr1NameDict[attrName] = 1
			
		concAttrList = attrList1

		for idx in range(numAttrList2):
			(attrName, x) = attrList2[idx]
			if attr1NameDict.has_key(attrName):
				attrName = attrName + '_2'
				attrList2[idx] = (attrName, x)
				print("Name conflict detected and resolved! attr[%d] = [%s]" % (idx,attrName))

		concAttrList.extend(attrList2)

		# Step 3, concatenate data feature list
		# attrList.append('%d %.1f' % (idx, freq))  # 1, means 'norminal'
		fe2IdxOffset = numAttrList1 # the offset for new attribute number in dataFeatureList2

		lenDataFeatureList = len(dataFeatureList1)
		assert(lenDataFeatureList == len(dataFeatureList2))

		concDataFeatureList = []
		for iData in range(lenDataFeatureList):
			dataFes1 = dataFeatureList1[iData]
			dataFes2 = dataFeatureList2[iData]

			newFeList = []
			# 1. assert two id are identical
			if dataFes1[0] != dataFes2[0]:
				print("Error! cannot combine two type feature for data %d" % iData)
				print(dataFes1)
				print(dataFes2)
				assert(False)

			newFeList.append(dataFes1[0])

			# 2. Then combine two feature
			# Copy the dataFes1 first, without any changing
			for iFe in range(1, len(dataFes1)):
				newFeList.append(dataFes1[iFe])

			# Then, append the dataFes2, with the index added by offset
			for iFe in range(1, len(dataFes2)):
				feStr = dataFes2[iFe]
				sp = feStr.split(' ')
				oriIdx = int(sp[0])
				oriValStr = sp[1]
				newFeList.append('%d %s' % (oriIdx + fe2IdxOffset, oriValStr))

			concDataFeatureList.append(newFeList)

		print("Concatenate completed!")
		print(len(concClassLable))
		print(len(concAttrList))
		print(len(concDataFeatureList))
			
		return(concClassLable, concAttrList, concDataFeatureList)

	def OutputArffFile(self, outArffPath, classLabelSet, \
										 attrList, dataFeatureList, featureType = "{0,1}"):
		"""
		Write arff file. This method is default method, and used by all
		derived classes

		@param arffPath: the output path
		@param classLabelSet: the list of class labels
		@param outArffPath: the list of attributes
		@param featureList: the list of features
		"""
		
		# Step.1 Initialize arff file writing
		ab = ArffBuilder()
		ab.StartWriting(outArffPath)
		relationStr = "text_file" # TODO other string will incur error!
		ab.WriteRelation(relationStr)

		# Step.2 Write attributes

		# Add class label attributes
		strClasses = '{' + ','.join(list(classLabelSet)) + '}'
		ab.AddAttr("CLASS_LABEL", strClasses)

		# Add other attributes
		#feType = '{0,1}' # should be norminal to save time
		tInt = type(1)
		for (word, typeStr) in attrList:
			if type(typeStr) == tInt:
				feType = featureType
			elif typeStr[0] == '{' or typeStr[1] == 'n':
				feType = typeStr
			else:
				feType = featureType
			ab.AddAttr(word, feType)
		ab.WriteAttr()

		# Step.3 Start writing data!
		nData = 0
		for d in dataFeatureList:
			if len(d) <= 1:
				continue
			ab.AddDataSparse(d)
			nData += 1
			
		lg = Log()
		#Done! write summary
		msg = "Done! Number of instance wrote: %d" % nData
		print(msg)
		lg.WriteLog(msg)

	def __processToken(self, tok):
		return tok

	def __init__(self):
		print("[%s] initialized!")

	def ExtractFeature(self, data):
		raise NotImplementedError("This is the base FeatureExtractor class! " \
														  "Please use any of the derived classes")


