import sys
sys.path.append('.')
sys.path.append('..')

from PosNgramExtractor import *
from ProdRuleExtractor import *
from NgramFeatureExtractor import *
from DepdExtractor import *

from Corpus.WritingData import *
from Corpus.SensData import *
from Corpus.SenTreeData import *
from Corpus.DependData import *

def ExtractAll():
	sensFile = '/home/xj229/data/3nat_lvl123_15K.sen'
	treeFile = '/home/xj229/data/3nat_lvl123_15K.tree'
	depdFile = '/home/xj229/data/3nat_lvl123_15K.depd'

	#sensFile = '/home/xj229/data/test1000.sen'
	sd = SensData()
	sd.Read(sensFile)
	
	
	# Extract ngram data
	fe1gram = NgramFeatureExtractor()
	fe1gram.SetNgramN(1)

	fe2gram = NgramFeatureExtractor()
	fe2gram.SetNgramN(2)

	(cls1, aList1, fList1) = fe1gram.ExtractFeature(sd.GetSensDict())
	(cls2, aList2, fList2) = fe2gram.ExtractFeature(sd.GetSensDict())

	arffPath = '/home/xj229/data/3nat_lvl123_15K.1gram.arff'
	fe1gram.OutputArffFile(arffPath, cls1, aList1, fList1)
	libsvmPath = arffPath + ".libsvm"
	fe1gram.ConvertArff2Libsvm(arffPath, libsvmPath)

	arffPath = '/home/xj229/data/3nat_lvl123_15K.2gram.arff'
	fe1gram.OutputArffFile(arffPath, cls2, aList2, fList2)
	libsvmPath = arffPath + ".libsvm"
	fe1gram.ConvertArff2Libsvm(arffPath, libsvmPath)

	## concatenate
	(clsSet, attrList, feList) = \
	fe1gram.ConcateTwoFeatureType(cls1, cls2, aList1, aList2, fList1, fList2)
	arffPath = '/home/xj229/data/3nat_lvl123_15K.12gram.arff'
	fe1gram.OutputArffFile(arffPath, clsSet, attrList, feList)
	libsvmPath = arffPath + ".libsvm"
	fe1gram.ConvertArff2Libsvm(arffPath, libsvmPath)
	
	# Extract POS data
	td = SenTreeData.GetInstance(treeFile)

	pne = PosNgramExtractor()
	(clsPos, attrPos, fePos) = pne.ExtractFeature(td.GetTreeDict())
	arffPath = '/home/xj229/data/3nat_lvl123_15K.POS.arff'
	fe1gram.OutputArffFile(arffPath, clsPos, attrPos, fePos)
	libsvmPath = arffPath + ".libsvm"
	fe1gram.ConvertArff2Libsvm(arffPath, libsvmPath)
	
	(clsSet, attrList, feList) = \
	fe1gram.ConcateTwoFeatureType(cls1, clsPos, aList1, attrPos, fList1, fePos)
	arffPath = '/home/xj229/data/3nat_lvl123_15K.1gram_POS.arff'
	fe1gram.OutputArffFile(arffPath, clsSet, attrList, feList)
	libsvmPath = arffPath + ".libsvm"
	fe1gram.ConvertArff2Libsvm(arffPath, libsvmPath)
	

	# Extract Prod rule feature
	
	prFe = ProdRuleExtractor()
	(clsPr, attrPr, fePr) = prFe.ExtractFeatureOnCorpus(td.GetTreeDict())
	arffPath = '/home/xj229/data/3nat_lvl123_15K.Pr.arff'
	fe1gram.OutputArffFile(arffPath, clsPr, attrPr, fePr)
	libsvmPath = arffPath + ".libsvm"
	fe1gram.ConvertArff2Libsvm(arffPath, libsvmPath)
	
	(clsSet, attrList, feList) = \
	fe1gram.ConcateTwoFeatureType(cls1, clsPr, aList1, attrPr, fList1, fePr)
	arffPath = '/home/xj229/data/3nat_lvl123_15K.1gram_Pr.arff'
	fe1gram.OutputArffFile(arffPath, clsSet, attrList, feList)
	libsvmPath = arffPath + ".libsvm"
	fe1gram.ConvertArff2Libsvm(arffPath, libsvmPath)

	dd = DependData.GetInstance(depdFile)

	# Extract ProdRule data
	

	# Extract Dependancy data


def ExtractPOS():
	sensFile = '/home/xj229/data/3nat_lvl123_15K.sen'
	treeFile = '/home/xj229/data/3nat_lvl123_15K.tree'
	depdFile = '/home/xj229/data/3nat_lvl123_15K.depd'

	td = SenTreeData.GetInstance(treeFile)

	sd = SensData()
	sd.Read(sensFile)
	fe1gram = NgramFeatureExtractor()
	fe1gram.SetNgramN(1)
	(cls1, aList1, fList1) = fe1gram.ExtractFeature(sd.GetSensDict())

	# POS 1
	pne1 = PosNgramExtractor()
	pne1.SetNgramN(1)
	(clsPos1, attrPos1, fePos1) = pne1.ExtractFeature(td.GetTreeDict())
	arffPath = '/home/xj229/data/3nat_lvl123_15K.POS1.arff'
	pne1.OutputArffFile(arffPath, clsPos1, attrPos1, fePos1)
	libsvmPath = arffPath + ".libsvm"
	pne1.ConvertArff2Libsvm(arffPath, libsvmPath)

	(clsSet, attrList, feList) = \
	pne1.ConcateTwoFeatureType(cls1, clsPos1, aList1, attrPos1, fList1, fePos1)
	arffPath = '/home/xj229/data/3nat_lvl123_15K.1gram_POS1.arff'
	pne1.OutputArffFile(arffPath, clsSet, attrList, feList)
	libsvmPath = arffPath + ".libsvm"
	pne1.ConvertArff2Libsvm(arffPath, libsvmPath)

	# POS 2
	pne2 = PosNgramExtractor()
	pne2.SetNgramN(2)
	(clsPos2, attrPos2, fePos2) = pne2.ExtractFeature(td.GetTreeDict())
	arffPath = '/home/xj229/data/3nat_lvl123_15K.POS2.arff'
	pne2.OutputArffFile(arffPath, clsPos2, attrPos2, fePos2)
	libsvmPath = arffPath + ".libsvm"
	pne2.ConvertArff2Libsvm(arffPath, libsvmPath)

	(clsSet, attrList, feList) = \
	pne2.ConcateTwoFeatureType(cls1, clsPos2, aList1, attrPos2, fList1, fePos2)
	arffPath = '/home/xj229/data/3nat_lvl123_15K.1gram_POS2.arff'
	pne2.OutputArffFile(arffPath, clsSet, attrList, feList)
	libsvmPath = arffPath + ".libsvm"
	pne2.ConvertArff2Libsvm(arffPath, libsvmPath)

	
	# POS 1+2
	(clsSet, attrList, feList) = \
	pne2.ConcateTwoFeatureType(clsPos1, clsPos2, attrPos1, attrPos2, \
														 fePos1, fePos2)
	arffPath = '/home/xj229/data/3nat_lvl123_15K.POS12.arff'
	pne2.OutputArffFile(arffPath, clsSet, attrList, feList)
	libsvmPath = arffPath + ".libsvm"
	pne2.ConvertArff2Libsvm(arffPath, libsvmPath)

	
if __name__ == '__main__':
	#ExtractAll()
	ExtractPOS()
