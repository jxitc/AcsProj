# Arff file parser
#

class ArffParser:
	"""
	Arff parser
	"""

	def __init__(self):
		self.__headerStr = ""
		self.__dataLines = []

	def Parse(self, filePath):
		fr = file.Path()
		
		self.__headerStr = ""
		self.__dataLines = []

		header = ""
		isInDataPart = False
		while True:
			line = fr.readline()
			if line == '':
				break

			if line.strip().lower() == "@data":
				isInDataPart = True
				continue
			
			if isInDataPart:
				self.__dataLines.append(line.strip())
			else:
				header += line
	
	def GetHeader():
		return self.__headerStr

	def GetDataLines():
		return self.__dataLines
	
	

	
				
				
			
			

		

		

