
class TreeNode:
	"""
	Tree Node class
	"""

	def __init__(self, si = -1, ei = -1, ct = None):
		self.__startIdx = si
		self.__end = ei
		self.__contentText = ct # i.e. "NP (PRP My) (NN name)"
		self.__headStr = None # i.e. "S1"
		self.__childList = [] # Child, point to other TreeNode

		self.__isTerminal = False

	def GetIsTerminalNode(self):
		return self.__isTerminal

	def SetIsTerminalNode(self, boolVal):
		self.__isTerminal = boolVal

	def SetChildList(self, childTnList):
		self.__childList = childTnList

	def SetHeadStr(self, hs):
		self.__headStr = hs.strip()

	def GetHeadStr(self):
		return self.__headStr

	def GetChildList(self):
		return self.__childList
	
	def GetContent(self):
		return self.__contentText

	def GetSplitPosWord(self):
		if self.__isTerminal:
			sp = self.__contentText.split(' ')
			return (sp[0], sp[1])
		else:
			print("Cannot split POS/Word for this node: %s" % self.__contentText)
			return (None, None)


class SenTreeReader:
	"""
	Tree reader to support following format:
	"(S1 (S (NP (PRP$ My) (NN name)) (VP (AUX 's) (ADJP (JJ Anfeng))) (. .)))"
	"""
	
#	def __getChildList(self, curTreeNodesDict, tgtText):

	def __outputTree(self, rootTn, depth = 0):
		"""
		Recursively output tree, recursive start
		"""
		
		indentStr = '  ' * depth
		# Print self first
		print(indentStr + rootTn.GetHeadStr())

		# Print child!
		childList = rootTn.GetChildList()

		for childTn in childList:
			self.__outputTree(childTn, depth + 1)

	def OutputTree(self, treeNode):
		"""
		Get readable string for a given tree node
		"""

		self.__outputTree(treeNode, 0)
		
	def GetPosWordsSequence(self, terminalList):
		"""
		Return the list of POS and words for given terminal node list
		i.e. "PRP I" to (PRP, I)
		"""
		posSeq = []
		wordSeq = []
		for tn in terminalList:
			(pos, word) = tn.GetSplitPosWord()
			assert(pos != None and word != None)
			posSeq.append(pos)
			wordSeq.append(word)

		assert(len(posSeq) == len(wordSeq))

		return (posSeq, wordSeq)


	def GetProdRuleList(self, rootNode):
		"""
		Return list of all production rule by traversing from the given
		rootNode
		i.e. "S=NP+VP"
		will ignore rule like S1, S2, etc...
		"""
		
		rsltRuleList = []

		if rootNode.GetIsTerminalNode():
			return [] # for terminal nodes, just return []

		# Step 1, record rule at this node first
		lSymb = rootNode.GetHeadStr() # left side symbol, i.e. 'S'
		rSymbs = [] # right side symbols, i.e. ['NP', 'VP']

		for childNode in rootNode.GetChildList():
			if childNode.GetIsTerminalNode():
				(pos, word) = childNode.GetSplitPosWord()
				rSymbs.append(pos)
			else:
				rSymbs.append(childNode.GetHeadStr())

		if lSymb != "S1" and lSymb != "S2" and len(rSymbs) > 0:
			newRule = "%s=%s" % (lSymb, '+'.join(rSymbs))
			rsltRuleList.append(newRule)

		# Step 2, recursively get rule from its children node
		childNodeProdList = []
		for childNode in rootNode.GetChildList():
			if not childNode.GetIsTerminalNode():
				childNodeProdList = self.GetProdRuleList(childNode)

		rsltRuleList.extend(childNodeProdList)

		# Step 3, Done! Return!
		return rsltRuleList
			
	def Scan(self, treeString):
		"""
		Parse input sentence tree string
		e.g. 
		 "(S1 (S (NP (PRP$ My) (NN name)) (VP (AUX 's) (ADJP (JJ Anfeng))) (. .)))"
		"""
		
		# Step 1: scan brackets
		stack = []

		lenStr = len(treeString)

		bracketPairs = []
		bpDict = {}

		for idx in range(lenStr):
			ch = treeString[idx]
			
			if ch == '(':
				stack.append(idx)
			elif ch == ')':
				openIdx = stack.pop()
				closeIdx = idx
				newPair = (openIdx, closeIdx)
				bracketPairs.append(newPair) 
				bpDict[openIdx] = newPair #Add to hashtable for quick looking up



		terminalNodeList = []

		# Step 2. Second pass scanning
		treeNodes = {}
		lastTn = None
		for bPair in bracketPairs:
			(openIdx, closeIdx) = bPair
			text = treeString[openIdx + 1 : closeIdx]
			newTn = TreeNode(openIdx, closeIdx, text)

			# Scan for embedded child node
			childList = []
			idx = openIdx + 1
			headStr = ""
			while idx < closeIdx:
				ch = treeString[idx]

				if ch == '(': # Encountering child node!
					(childOpenIdx, childCloseIdx) = bpDict[idx]
					childTn = treeNodes[idx]
					childList.append(childTn)
					idx = childCloseIdx
				else:
					headStr += ch

				idx += 1

			newTn.SetHeadStr(headStr.strip())
			newTn.SetChildList(childList)
			if len(childList) == 0:
				newTn.SetIsTerminalNode(True)
			else:
				newTn.SetIsTerminalNode(False)
				

			treeNodes[openIdx] = newTn
			if newTn.GetIsTerminalNode():
				terminalNodeList.append(newTn)

			lastTn = newTn

		# Will return the root tree node, as well as a list of all
		# terminal node
		return (lastTn, terminalNodeList) 



	def __destroy(self, rootTn):
		"""
		Recursively destroy the tree, and return the number of tree node destroyed
		"""

		childList = rootTn.GetChildList()

		# Del all child first
		nChild = 0
		for childNode in childList:
			nChild += self.__destroy(childNode)
			
		# and delete self
		del rootTn
		return nChild + 1
		
	def Destroy(self, rootTn):
		"""
		Recursively destroy the tree
		"""
		
		totalDestroyed = self.__destroy(rootTn)
		return totalDestroyed


		

def main():
	s = "(S1 (S (NP (PRP$ My) (NN name)) (VP (AUX 's) (ADJP (JJ Anfeng))) (. .)))"
	s = "(S1 (S (VP (VB Line) (PRT (RP up)) (NP (DT the) (NNS bottles)) (PP (IN in) (NP (NP (NNS rows)) (PP (IN of) (NP (NP (CD 4)) (, ,) (ADVP (RB then)) (NP (CD 3)) (, ,) (NP (NP (RB then) (JJ 1-just)) (PP (IN like) (NP (NN ten-pin) (NN bowling))))))))) (. .)))"

	stReader = SenTreeReader()

	fn = '/mnt/scratch/xj229/data/20120220_senssel_CJ.dat.pcjr'
	fr = open(fn, 'r')
	
	nLine = 0
	for line in fr.readlines():
		(rt, terminals) = stReader.Scan(line.strip())
		stReader.OutputTree(rt)
		for t in terminals:
			print("%s: %s" % (t.GetHeadStr(), t.GetContent()))

		(posSeq, wordSeq) = stReader.GetPosWordsSequence(terminals)
		print(posSeq)
		print(wordSeq)
		
		prodRuleList = stReader.GetProdRuleList(rt)
		print(prodRuleList)

		nLine += 1
		if nLine % 1000 == 0:
			print("Processed %d lines" % nLine)

		numDestroyed = stReader.Destroy(rt)
		#numDestroyed = 1
		print("Destroyed: #node = %d" % numDestroyed)

		print([t.GetContent() for t in terminals])
		raw_input('Pause ... ')

	stReader.Scan(s)

if __name__ == '__main__':
	import cProfile
	cProfile.run('main()')
