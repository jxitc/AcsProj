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
	cnt = 0


	def __init__(self):
	
		if Log.RunLogFilePath == "":
			# TODO or read log path from config file?
			from ConfigFile import ConfigFile
			cf = ConfigFile()
			Log.RunLogFilePath = cf.GetConfig("RUNLOGFILE")

		else:
			pass

		if Log.RunLogWriter is None:
			Log.RunLogWriter = open(self.RunLogFilePath, 'a') # Start appending
		
			print("Start Logging")
			Log.RunLogWriter.write( \
			 "\n\n======================================================\n" \
			 "*********************************************************\n"  \
			 "Start logging %s\n %s\n\n" \
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

		Log.RunLogWriter.write("[%s]\t%s\n" % (self.GetTimeStamp(), msg))
		Log.RunLogWriter.flush()

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
