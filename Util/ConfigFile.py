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
		

		for line in fr.readlines():
			line = line.strip()
			if line == "":
				continue
			
			if line[0] != '#': # ignore lines start by #
				sp = line.split('=')
				if len(sp) == 2:
					key = sp[0].strip()
					val = sp[1].strip()
					self.__configDict[key] = val
				else:
					self.__print("Ignore config line: " + line)

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

	def GetConfig(self, confKey):
		confKey = confKey.strip()
		if not self.__configDict.has_key(confKey):
			print("Error! Config not found for: " + confKey)
			return None
		else:
			return self.__configDict[confKey]

				



# self testing
if __name__ == '__main__':
	print('Start module self testing ... ')
	cf = ConfigFile()
	print(cf.GetConfigListStr())
	print("cf2:")
	cf2 = ConfigFile()
	print(cf2.GetConfigListStr())


		
			
			
