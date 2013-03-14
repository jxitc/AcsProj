import re

class Tokenizer:
	"""
	Tokenizer class
	"""

	__instance = None
	

	@staticmethod
	def GetInstance():
		if Tokenizer.__instance is None:
			Tokenizer.__instance = Tokenizer()
			print("Tokenzier instance initilized")

		return Tokenizer.__instance

	@staticmethod
	def Split(sen):
		tkz = Tokenizer.GetInstance()
		return tkz.__split(sen)

	def __init__(self):
		"""
		Constructor
		"""
		pat = r'["\.,:;?!\(\)\[\]\<\>' + r"']"
		self.__rexPunct = re.compile(pat)
		self.__rexSpace = re.compile(r'\s+')
		self.__repPunctStr = r' '

		
	def __split(self, sen):
		"""
		Split given sentcen. Return a set of tokens
		"""

		# First, replace punctuation
		sen = self.__rexPunct.sub(self.__repPunctStr, sen)
		#print sen

		# Split
		sp = self.__rexSpace.split(sen)

		# Process contiguous spaces
		lenSp = len(sp)

		for i in range(lenSp, 0, -1):
			idx = i - 1
			c = sp[idx].strip()
			if c == '' or c == None:
				del sp[idx]

		return sp

def main():
	while(True):
		s = raw_input("Input:")
		print(Tokenizer.Split(s))

if __name__ == '__main__':
	main()
