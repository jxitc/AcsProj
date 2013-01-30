# This class builds ARFF file from scratch
# http://weka.wikispaces.com/ARFF+%28book+version%29

class ArffBuilder():

	Type_Numeric = "NUMERIC"
	Type_Integer = "INTEGER"
	Type_Real = "REAL"
	Type_String = "STRING"


	def __init__(self):
		self.__outDir = ""
		self.__outFw = None

		self.__attributes = []
		self.__classes = []

		self.__validTypes = [self.Type_Numeric, self.Type_Integer,
												 self.Type_Real, self.Type_String]

		self.__isHeadWrote = False
		self.__isRelationWrote = False
		self.__isAttrWrote = False
		self.__isDataWrote = False

		self.__useSparseFormat = True

	def GetNumAttr(self):
		return len(self.__attributes)

	def GetNumClass(self):
		return len(self.__classes)

	def __isListContain(self, list, tgt):

		for e in list:
			if e == tgt:
				return True

		return False
	
	def StartWriting(self, outFileName):
		if not self.__outFw is None:
			return

		self.__outFw = open(outFileName, 'w')
		print("Start writing .arff file to %s" % outFileName)


	def __isValidType(self, type):
		return self.__isListContain(self.__validTypes, type)

	def WriteRelation(self, relName):
		if self.__isRelationWrote == True:
			return

		self.__outFw.write("@relation %s\n\n" % relName)
		self.__isRelationWrote = True

	def WriteAttr(self):
		if self.__isAttrWrote == True:
			return

		for attr in self.__attributes:
			self.__outFw.write("@attribute %s %s\n" % (attr[0], attr[1]))

		self.__outFw.write("\n")
		self.__outFw.flush()

		self.__isAttrWrote = True

	def AddAttr(self, attrName, attrType):
		#assert(self.__isValidType(attrType))
		self.__attributes.append((attrName, attrType))

	def AddData(self, attrList):
		if attrList == []:
			return

		if not self.__isDataWrote:
			self.__outFw.write("\n\n@data\n")
			self.__isDataWrote = True

		# write data entry
		outStr = ""
		for fe in attrList:
			outStr += "%s, " % fe
		outStr = outStr[0:-2]
		self.__outFw.write(outStr + "\n")

		

	def AddDataSparse(self, feaList):
		"""
		Assume data is following format:
		[
			(idx, val),
			(idx, val),
			....
		]
		"""
		# Asssume the passed-in data is also sparse format
		nAttr = self.GetNumAttr()
		for fea in feaList:
			feaIdx = fea[0]
			feaVal = fea[1]
		

	def WriteArffHeader(self):
		assert(self.__attrbiutes != [] and self.__classes != [])
		"""
 	 % 1. Title: Iris Plants Database
   % 
   % 2. Sources:
   %      (a) Creator: R.A. Fisher
   %      (b) Donor: Michael Marshall (MARSHALL%PLU@io.arc.nasa.gov)
   %      (c) Date: July, 1988
   % 
   @RELATION iris
 
   @ATTRIBUTE sepallength  NUMERIC
   @ATTRIBUTE sepalwidth   NUMERIC
   @ATTRIBUTE petallength  NUMERIC
   @ATTRIBUTE petalwidth   NUMERIC
   @ATTRIBUTE class        {Iris-setosa,Iris-versicolor,Iris-virginica}
		"""

		headStr = ""
		self.__outFw.write(headStr)
		self.__outFw.flush()
		self.__isHeadWrote = True
