'''
Created on 30 Jan 2013

@author: xj229
'''


class Log:
	"""
	Log class, use to log files 
	"""
	# class static variable
	RunLogFilePath = "" 
	RunLogWriter = None


	def __init__(self):
		
		if self.RunLogFilePath == "":
			# TODO or read log path from config file?
			from ConfigFile import ConfigFile
			cf = ConfigFile()
			self.RunLogFilePath = cf.GetConfig("RUNLOGFILE")
			
		else:
			pass

		if self.RunLogWriter is None:
			self.RunLogWriter = open(self.RunLogFilePath, 'a') # Start appending
		
		print("Start Logging")
		self.RunLogWriter.write( \
			"\n\n===============================\n Start logging %s\n %s\n\n" \
			% (self.GetDateStamp(), __file__) \
		)
		
	
	def GetDateStamp(self):
		"""
		Get current datetime stamp.
		"""
		
		import time
		timeFmt = "%Y%m%d%H%M%S"
		timeStr = time.strftime(timeFmt, time.localtime())
		return timeStr

	def GetTimeStamp(self):
		"""
		Get current time stamp.
		"""

		import time
		timeFmt = "%H.%M.%S"
		timeStr = time.strftime(timeFmt, time.localtime())
		return timeStr

	def WriteLog(self, msg):
		"""
		Write message to log file
		"""

		self.RunLogWriter.write("[%s]\t%s\n" % (self.GetTimeStamp(), msg))
		



# Testing...
if __name__ == '__main__':
	print('Start module self testing ... ')
	lg = Log()
	lg.WriteLog("This is a log message")
	lg2 = Log()
	lg2.WriteLog("LG2: I am here!")
	lg.WriteLog("This is another log message")
	lg.WriteLog("This is another log message")
	lg.WriteLog("This is another log message")
	lg.WriteLog("This is another log message")
