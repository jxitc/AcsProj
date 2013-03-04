'''
Created on 21 Feb 2013

@author: xj229
'''
import time
import resource

class Timer:
	"""
	Timer class
	"""

	def __init__(self):
		self.__times = []
		self.__startTime = self.__now()
		self.__endTime = None

	def __now(self):
		return time.time()

	def Tick(self):
		self.__times.append(self.__now)

	def GetLastTickDuration(self):
		if len(self.__times) < 2:
			return None

		t1 = self.__times[-1]
		t2 = self.__times[-2]

		return t1 - t2

	def Start(self):
		self.__startTime = self.__now()

	def Stop(self):
		self.__endTime = self.__now()

	def GetStartEndTime(self):
		s = self.__startTime
		e = self.__endTime
		assert(e >= s)
		return e - s
	

class Perfmon:
	"""
	Perfomance monitor, to get time / memory usage of 
	python programme
	"""

	def __init__(self):
		"""
		Constructor
		"""
		self.__timer = Timer()
		self.__status = 'NULL'
		
		self.__startRu = None # start resrouce usage
		self.__endRu = None # start resrouce usage

	def __getResourceUsage(self):
		"""
		RUSAGE_SELF: for this process only (not include subprocess.call(...)
		RUSAGE_CHILD: Child process only, i.e. subprocess.call()
		RUSAGE_BOTH: both, but may not working on some system
		"""
		return resource.getrusage(resource.RUSAGE_CHILDREN)

	def Start(self):
		print("Performance Monitor start working!!")
		self.__status = 'Started'
		self.__timer.Start()
		self.__startRu = self.__getResourceUsage()
	
	def Stop(self):
		print("Performance Monitor stopped working!!")
		self.__status = 'Stopped'
		self.__timer.Stop()
		self.__endRu = self.__getResourceUsage()

	def GetRuageStr(self, ruData):
		rsltStr = ""

		for attrStr in dir(ruData):
			if attrStr.find('__') == 0:
				continue

			attrVal = ruData.__getattribute__(attrStr)
			rsltStr += "%s ->\t%s\n" % (attrStr, attrVal)

		return rsltStr

	def GetSummary(self):

		if self.__status != 'Stopped':
			print("Perform monitor not stopped, status: %s" % self.__status)
			return ""

		# Timing summary
		rsltString = "\n\nPerfmon Summary:\n"
		rsltString += "Time Used(s): %f" % self.__timer.GetStartEndTime()

		# Mem summary
		sMem = self.__startRu.ru_maxrss / 1024
		eMem = self.__endRu.ru_maxrss / 1024
		diffMem = eMem - sMem
    		rsltString += "\nMemory Used (Mb): %f" % diffMem

		
		rsltString += """
=========== Prev Mem ============
%s
=========== ======== ============
		""" % self.GetRuageStr(self.__startRu)
		
		rsltString += """
=========== After Mem ===========
%s
=========== ======== ============
		""" % self.GetRuageStr(self.__endRu)

		return rsltString
		
