# Read main writing file like:
# 
# WritingId MemberId  Essay DateSubmitted Grade Comment topicId correctedWritin
# 1 18428834  Let's arrange an area of 8 metres by 3 metres as the "bowling all
#

#from var import *

import sys
sys.path.append('.')
sys.path.append('..')

import operator

from Util.ConfigFile import *


class WritingData(object):
	""" 
	class to load writing metadata
	"""

	# Singleton Instance definition
	__instance = None
	__refCount = 0
	
	@staticmethod
	def GetInstance():
		# TODO need to forbit the using of constructing function
		if WritingData.__instance is None:
			# ok, first time use, initial new
			cf = ConfigFile()
			wdPath = cf.GetConfig("WRITINGDATA")
			WritingData.__instance = WritingData()
			WritingData.__instance.Read(wdPath)
			print("WritingData instance initialized")

		return WritingData.__instance
	
	def __init__(self):
		self.__colName = {}
		self.__data = {} # wid: [col1.. col2 ..]
		self.__dataFileName = ""

	def GetColNames(self):
		sortedCN = sorted(self.__colName.iteritems(), key=operator.itemgetter(1))
		return sortedCN

	def GetDictColName(self):
		return self.__colName

	def GetDictData(self):
		return self.__data

	def Read(self, dataFn):
		self.__dataFileName = dataFn
		f = open(dataFn, 'r')
		
		#assuming first line is
		firstLine = f.readline().strip()
		cols = firstLine.split('\t')
		print(cols)
	
		# initialize column names
		idx = 0
		colName = {}
		for col in cols:
			colName[col] = idx
			idx += 1
	
		line = f.readline()
		while line:
			line = line.strip()
			splt = line.split('\t')

			# Store data
			wid = int(splt[0])
			self.__data[wid] = splt

			line = f.readline()

		self.__colName = colName

		f.close()
		
		print("Load completed! %d data read.\n" % len(self.__data))
		
	def GetData(self, wid):
		if self.__data.has_key(wid):
			return self.__data[wid]
		else:
			print("No data matches %d!\n" % wid)
			return None
	
	def GetValueByWid(self, wid, colStr):
		wid = int(wid)
		data = self.GetData(wid)
		return self.GetValue(data, colStr)

	def GetValue(self, data, colStr):
		if not self.__colName.has_key(colStr):
			print("Incorrect colunmn string: %s\n" % colStr)
			return None

		colId = self.__colName[colStr]
		return data[colId]

	def GetUniqueData(self, colStr):
		"""
		Return a set of unique value for given colStr
		to Lower!!!
		"""
		colId = self.__colName[colStr]
		vals = {}
		for d in self.__data.values():
			newVal = d[colId].lower()
			if newVal == "":
				continue
			vals[newVal] = 1

		return vals.keys()

	def GetStat(self, colStr):
		"""
		Get statistics information about the data
		"""
		colIdx = self.__colName[colStr]
		count = {}
		for d in self.__data.values():
			newVal = d[colIdx].lower().strip()
			if newVal == "":
				continue
			else:
				if count.has_key(newVal):
					count[newVal] += 1
				else:
					count[newVal] = 1

		sortedCnt = sorted(count.iteritems(), \
										  key=operator.itemgetter(1), \
											reverse = True)
		return sortedCnt
			

def main():
	w1 = WritingData.GetInstance()
	w2 = WritingData.GetInstance()
	
	print("============")

	print w1
	print w2

	print(id(w1))
	print(id(w2))
	
if __name__ == '__main__':
	main()



