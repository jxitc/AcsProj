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
		
	def OutputArffFile(self, outArffPath, classLabelSet, \
												   attrList, dataFeatureList):
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
		feType = '{0,1}' # should be norminal to save time
		for (word, freq) in attrList:
			ab.AddAttr(word, feType)
		ab.WriteAttr()

		# Step.3 Start writing data!
		nData = 0
		for d in dataFeatureList:
			ab.AddDataSparse(d)
			nData += 1
			
		lg = Log()
		#Done! write summary
		msg = "Done! Number of instance wrote: %d" % nData
		print(msg)
		lg.WriteLog(msg)

	def __init__(self):
		print("[%s] initialized!")

	def ExtractFeature(self, data):
		raise NotImplementedError("This is the base FeatureExtractor class! " \
														  "Please use any of the derived classes")
