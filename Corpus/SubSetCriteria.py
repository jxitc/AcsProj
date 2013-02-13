'''
Created on 2013-2-7

@author: Xiao
'''
	
class SubSetCriteria:
	def __init__(self):
		self.__criSet = {} # i.e. ["levelNo":[1,2,3,4]; 
											 #			 "Nationality":['cn', 'fr'] ... etc.
											 #			]
		self.__wd = None
		self.__colName = {}

	def AddCriteria(self, colStr, criVal):
		valSet = []
		if self.__criSet.has_key(colStr):
			valSet = self.__criSet[colStr]
		valSet.append(criVal)
		self.__criSet[colStr] = valSet
	
	
	def SetWritingDataObj(self, wdObj):
		self.__wd = wdObj
		self.__colName = self.__wd.GetDictColName()

	def GetSummaryStr(self):
		"""
		Get a string of description of current defined criteria
		"""

		rsltStr = "\nSubSetCriteria Summary:\n"
		for colCri in self.__criSet.keys():
			rsltStr += colCri + "\t["

			valSet = self.__criSet[colCri]
			if valSet == []:
				continue

			valStr = ""
			for v in valSet:
				valStr += "%s, " % v

			valStr = valStr.strip() # remove trailing space
			valStr = valStr[0:-1]		# remove last comma ','

			rsltStr += valStr + "]\n"

		return rsltStr
			


	def Test(self, data):
		"""
		Test if given data is accordance with the pre-defined
		crateira
		"""
		assert(self.__wd != None)
		assert(self.__criSet != {})

		for colCri in self.__criSet.keys():
			colStr = colCri
			criValSet = self.__criSet[colStr]
			colId = self.__colName[colStr]
			tgtVal = data[colId]

			# test if the data is equal to any of the
			# value in criValSet
			anyCri = False
			for val in criValSet:
				if str(val) == str(tgtVal):
					anyCri = True
					break
	
			if anyCri == False: # none of the value satisfied the criteria
				return False

		return True