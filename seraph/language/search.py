from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset

def getSynsets(word: str) -> list[Synset]:
	return wn.synsets(word)

def getHypernyms(ss: Synset, depth: int=5) -> list[Synset]:
	output = ss.hypernyms()
	
	for _ in range(depth):
		for hyper in output:
			for newHypernym in hyper.hypernyms():
				if newHypernym not in output:
					output.append(newHypernym)
					
	return output

def getHyponyms(ss: Synset, depth: int=5) -> list[Synset]:
	output = ss.hyponyms()

	for _ in range(depth):
		for hypo in output:
			for newHyponym in hypo.hyponyms():
				if newHyponym not in output:
					output.append(newHyponym)

	return output
