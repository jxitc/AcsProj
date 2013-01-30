# This script used to generate bag of words

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'CorpProc'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Training'))
sys.path.append(os.path.dirname(__file__))

from WritingData import *
from Vocab import *
from SensData import *
from ArffBuilder import *

import operator

def GenerateBog():
	# generate bog arff file.

	wd = WritingData()
	wd.Read(HomeData + "/writing_all_shrinked.dat")
	sd = SensData()
	sd.Read(DataFolder + "/20120220_senssel.dat")
	ab = ArffBuilder()

	vocab = Vocab()
	vocab.Read(HomeData + "/Training/sens_alpha_num.vocab")

	ab.StartWriting(HomeData + "/bog_beforefilter_cutoff50.arff")
	ab.AddAttr("text", "String")

	strNatClasses = "{"
	for n in wd.GetUniqueData("Nationality"):
		if n == "":
			continue
		strNatClasses += "%s," % n
	strNatClasses = strNatClasses[0:-1] + "}"
	ab.AddAttr("nationality", strNatClasses)

	ab.WriteRelation("text_files")
	ab.WriteAttr()


	sd.ResetWritingIter()
	(wrtId, wrt) = sd.GetNextWriting()
	allToks = 0
	afterPrunedToks = 0
	while wrt:
		nat = wd.GetValueByWid(wrtId, "Nationality").lower()
		if nat.strip() == "":
			(wrtId, wrt) = sd.GetNextWriting()
			continue

		for sen in wrt:
			doPrune = True
			cutOffCnt = 50
			# do prune!

			allToks += len(sen.split(" "))
			if doPrune:
				sp = sen.split(" ")
				newSens = []

				for tok in sp:
					if not tok.isalpha():
						newSens.append(tok)
						continue
					
					fre = vocab.GetFrequency(tok)
					#print("freq(%s) = %d" % (tok, fre))
					if fre >= cutOffCnt:
						newSens.append(tok)
					#else:
					#	print("Pruned: " + tok)

				sen = " ".join(newSens)
				sen = sen.strip()
			
			afterPrunedToks += len(sen.split(" "))

			attrList = ['"%s"' % sen, nat]
			ab.AddData(attrList)
			
		(wrtId, wrt) = sd.GetNextWriting()

	print("Prune Result: %s / %s retained" % (allToks, afterPrunedToks))
	

def GenerateBog_beforeFilter():
	# generate bog arff file. Before filter, i.e. transfer to
	# word vector
	wd = WritingData()
	wd.Read(HomeData + "/writing_all_shrinked.dat")
	sd = SensData()
	sd.Read(DataFolder + "/20120220_senssel.dat")
	ab = ArffBuilder()

	vocab = Vocab()
	vocab.Read(HomeData + "/Training/sens_alpha_num.vocab")

	ab.StartWriting(HomeData + "/bog_beforefilter_cutoff6.arff")
	ab.AddAttr("text", "String")

	strNatClasses = "{"
	for n in wd.GetUniqueData("Nationality"):
		if n == "":
			continue
		strNatClasses += "%s," % n
	strNatClasses = strNatClasses[0:-1] + "}"
	ab.AddAttr("nationality", strNatClasses)

	ab.WriteRelation("text_files")
	ab.WriteAttr()


	sd.ResetWritingIter()
	(wrtId, wrt) = sd.GetNextWriting()
	allToks = 0
	afterPrunedToks = 0
	while wrt:
		nat = wd.GetValueByWid(wrtId, "Nationality").lower()
		if nat.strip() == "":
			(wrtId, wrt) = sd.GetNextWriting()
			continue

		for sen in wrt:
			doPrune = True
			cutOffCnt = 6
			# do prune!

			allToks += len(sen.split(" "))
			if doPrune:
				sp = sen.split(" ")
				newSens = []

				for tok in sp:
					if not tok.isalpha():
						newSens.append(tok)
						continue
					
					fre = vocab.GetFrequency(tok)
					#print("freq(%s) = %d" % (tok, fre))
					if fre >= cutOffCnt:
						newSens.append(tok)
					#else:
					#	print("Pruned: " + tok)

				sen = " ".join(newSens)
				sen = sen.strip()
			
			afterPrunedToks += len(sen.split(" "))

			attrList = ['"%s"' % sen, nat]
			ab.AddData(attrList)
			
		(wrtId, wrt) = sd.GetNextWriting()

	print("Prune Result: %s / %s retained" % (allToks, afterPrunedToks))
	


def GenerateBog_CrossValidation():
	# generate bog arff file. Before filter, i.e. transfer to
	# word vector
	wd = WritingData()
	wd.Read(HomeData + "/writing_all_shrinked.dat")
	sd = SensData()
	sd.Read(DataFolder + "/20120220_senssel.dat")
	ab = ArffBuilder()

	vocab = Vocab()
	vocab.Read(HomeData + "/Training/sens_alpha_num.vocab")

	ab.StartWriting(HomeData + "/bog_cv1_trn.arff")
	ab.AddAttr("text", "String")

	strNatClasses = "{"
	for n in wd.GetUniqueData("Nationality"):
		if n == "":
			continue
		strNatClasses += "%s," % n
	strNatClasses = strNatClasses[0:-1] + "}"
	ab.AddAttr("nationality", strNatClasses)

	ab.WriteRelation("text_files")
	ab.WriteAttr()

	allSens = sd.GetAllSentencesWrtId()
	nSens = len(allSens)
	trnRatio = 0.9
	numTrn = trnRatio * float(nSens)
	numTst = nSens - numTrn

	iSen = 0
	print("Start Writing Training...")
	while iSen < numTrn:
		(wrtId, sen) = allSens[iSen]
		nat = wd.GetValueByWid(wrtId, "Nationality").lower()
		#Do prune? TODO
		attrList = ['"%s"' % sen, nat]
		ab.AddData(attrList)
		iSen += 1


	ab2 = ArffBuilder()
	ab2.StartWriting(HomeData + "/bog_cv1_tst.arff")
	ab2.AddAttr("text", "String")
	ab2.AddAttr("nationality", strNatClasses)
	ab2.WriteRelation("text_files")
	ab2.WriteAttr()

	print("Start Writing Testing...")
	while iSen < nSens:
		(wrtId, sen) = allSens[iSen]
		nat = wd.GetValueByWid(wrtId, "Nationality").lower()
		attrList = ['"%s"' % sen, nat]
		ab2.AddData(attrList)
		iSen += 1
	
def GenerateVocab():
	#fn = HomeData + "/senssel.dat"
	fn = DataFolder + "/20120220_senssel.dat"
	fwn = HomeData + "/Training/sens_alpha_lower.vocab"

	fwVocab = open(fwn, 'w')

	sd = SensData()
	sd.Read(fn)

	sens = sd.GetAllSentences()

	i = 0
	wrds = {}
	for sen in sens:
		wrdsInSen = sen.split(' ')
		for wrd in wrdsInSen:
			wrd = wrd.strip()

			if not wrd.isalpha():
				continue

			if wrd == "":
				continue

			wrd = wrd.upper()

			if wrds.has_key(wrd):
				wrds[wrd] += 1
			else:
				wrds[wrd] = 1

			i = i + 1
	print(len(wrds))
	# Sort vocab:
	sortedList = sorted(wrds.iteritems(), key=operator.itemgetter(1), reverse=True)
	
	for s in sortedList:
		fwVocab.write("%s\t%s\n" % (s[0],s[1]))

	fwVocab.flush()
	fwVocab.close()
		
# GenerateVocab()


GenerateBog_CrossValidation()
