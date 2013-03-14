# -*- coding: utf-8 -*-

import sys,os
sys.path.append('../')
sys.path.append('./')

from Corpus.WritingData import *
from Corpus.Vocab import *
from Corpus.SensData import *

from Util.Log import *
from Util.ConfigFile import *
from Util.PorterStemmer import *
from Util.Perfmon import *

from Weka.ArffBuilder import *
from Weka.ArffParser import *

from Script.WekaSh import *

class BogFeatureExtractor(FeatureExtractorBase):
	"""
	Bag-of-words feature extractor
	"""

	Description = "BogFeatureExtractor"

	def ExtractFeature(self, sentenceList):
		"""
		Extract the bag-of-words feature from a list of sentence.
		Get the vocabulary first, and then trying to generate the bag of words 
		feature
		"""

		return None

	
