# Read main writing file like:
# 
# WritingId MemberId  Essay DateSubmitted Grade Comment topicId correctedWritin
# 1 18428834  Let's arrange an area of 8 metres by 3 metres as the "bowling all
#

#from var import *
import operator

class WritingData:
	""" 
	class to load writing metadata
	"""

	def __init__(self):
		self.__colName = {}
		self.__data = {}
		self.__dataFileName = ""

	def GetColNames(self):
		sortedCN = sorted(self.__colName.iteritems(), key=operator.itemgetter(1))
		return sortedCN

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
			

#def ShrinkFile(wrtFile, outFile = ""):
#	f = open(wrtFile, 'r')
#	
#	if outFile == "":
#		outFile = wrtFile + ".srk"
#	
#	fw = open(outFile, 'w')
#	
#	#assuming first line is
#	firstLine = f.readline().strip()
#	cols = firstLine.split('\t')
#	print cols
#
#	print "Now Shrink to following columns:\n"
#
#	cIds = [0,1,3,4,6,8,9,10,11,13]
#	print(cIds)
#	outStr = ""
#	for id in cIds:
#		outStr =  outStr + str(cols[id]) + '\t'
#	outStr = outStr.strip() + '\n'
#	fw.write(outStr)
#	
#
#	# initialize column names
#	idx = 0
#	for col in cols:
#		colName[col] = idx
#		idx += 1
#	
#	line = f.readline()
#	times = 0
#	while line:
#		line = line.strip()
#		vals = line.split('\t')
#		outStr = ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % \
#								(vals[0],vals[1],vals[3], vals[4], vals[6], \
#								 vals[8],vals[9],vals[10],vals[11],vals[13]) \
#						 )
#		fw.write(outStr)
#		line = f.readline()
#
#		times += 1
#		if times % 100 == 0:
#			fw.flush()
#
#	fw.flush()
#	fw.close()
#
#	print("Shrink Done! %d lines shrinked to %s !\n" % (times, outFile))

#fn = "../../data/writing.dat"
#ShrinkFile(fn)
#ShrinkFile(WritingFile, HomeData + "/writing_all_shrinked.dat")
