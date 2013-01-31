'''
Created on 2013-1-31

@author: Xiao

'''


class ConfigFile():
	"""
	This provide basic config file accessing
	"""
	
	# Static variables
	import os
	__configDict = {} 
	__configFilePath = os.path.join(os.path.dirname(__file__), \
																	'../conf/config.ini')

	def __init__(self):
		"""
		Constructor
		"""

		if self.__configDict != {}:
			return

		self.__readConfig()

	
	def __readConfig(self):
		"""
		Read configs from config file
		"""

		fr = open(self.__configFilePath, 'r')
		
		line = fr.readline().strip()

		while(line):
			if line[0] != '#': # ignore lines start by #
				sp = line.split('=')
				if len(sp) == 2:
					key = sp[0]
					val = sp[1]
					self.__configDict[key] = val
				else:
					self.__print("Ignore config line: " + line)
				
			line = fr.readline().strip()

		self.__print("Read configs from: %s\n%d configs read!" \
								 % (self.__configFilePath, len(self.__configDict)) \
								)

		fr.close()

	def GetConfigListStr(self):
		"""
		Get configuration list string
		"""
		if self.__configDict == {}:
			return ""

		rsltStr = ""
		for k in self.__configDict.keys():
			rsltStr += "%s = %s\n" % (k, self.__configDict[k])

		return rsltStr.strip()

	def __print(self, msg):
		print("[ConfigFile] " + msg)



# self testing
if __name__ == '__main__':
	print('Start module self testing ... ')
	cf = ConfigFile()
	print(cf.GetConfigListStr())
	print("cf2:")
	cf2 = ConfigFile()
	print(cf2.GetConfigListStr())


		
			
			
