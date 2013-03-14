# Base class definition for Feature Extractor

class FeatureExtractorBase:
	"""
	Providing unified feature extraction interface
	"""
	
	Description = "FeatureExtractorBase"

	def __init__(self):
		print("[%s] initialized!")
		

	def ExtractFeature(self, data):
		raise NotImplementedError("This is the base FeatureExtractor class! " \
														  "Please use any of the derived classes")

	
