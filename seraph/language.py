# THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE
# PUBLIC LICENSE ("AGREEMENT"). ANY USE, REPRODUCTION OR DISTRIBUTION
# OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT.

from seraph import entity
from seraph import reaction
from seraph import utils

with utils.Indent():
	print("Importing NLTK ...")
	import nltk
	print("Importing wordnet ...")
	from nltk.corpus import wordnet
	print("Importing framenet ...")
	from nltk.corpus import framenet
	print("Importing pos_tag ...")
	from nltk.tag import pos_tag
	print("Importing word_tokenize ...")
	from nltk.tokenize import word_tokenize
	print("Importing sent_tokenize ...")
	from nltk.tokenize import sent_tokenize
	print("Importing vader ...")
	from nltk.sentiment import vader
	print("Importing opinion lexicon ...")
	from nltk.corpus import opinion_lexicon
	print("NLTK imported.")

NEGATIVITY = "negativity"
NEUTRALITY = "neutrality"
POSITIVITY = "positivity"

def lemmas(string: str) -> list[object]:
	output = []
	for ss in wordnet.synsets(string):
		for lemma in ss.lemmas():
			output.append(lemma)
	return output

def synonyms(string: str) -> list[str]:
	

def sentiment(string: str) -> tuple[float, list[str], float, float, list[str], float]:
	"""
	Use the VADER sentiment analysis tool to analyze a sentence.
	Returns a sextuple of the negativity of the sentence, negative words in the sentence, the
	neutrality of the sentence, the positivity of the sentence, positive words in the sentence,
	and the modification by compounding, all as floats or lists of strings where applicable.
	"""
	sid = vader.SentimentIntensityAnalyzer()
	result = sid.polarity_scores(string)
	return (result["neg"], [s for s in string if s in opinion_lexicon.negative()], result["neu"], result["pos"], [s for s in string if s in opinion_lexicon.positive()], result["compound"])

class TagGroup:
	def __init__(self, *tags: list[str]):
		self.tags = tags

	def __repr__(self) -> str:
		return "<seraph.language.TagGroup of " + ", ".join(self) + ">"
	
	def __len__(self) -> int:
		return len(self.pos)
	
	def __iter__(self) -> object:
		self.n = -1
		return self
	
	def __next__(self) -> str:
		self.n += 1
		if self.n >= len(self):
			raise StopIteration
		return self.tags[self.n]
	
	def __contains__(self, tag: str) -> bool:
		return tag in self.tags
	
	def __rshift__(self, sent: list[tuple[str, str]]) -> list[list[str]]:
		output = []
		current = []
		for word, tag in sent:
			if tag in self:
				current.append(word)
			else:
				if len(current) > 0:
					output.append(current)
					current = []
		return output

linguisticTagGroups = {
	None: None
	# fill this in please
}	

class Tokenization(entity.Entity):
	def __init__(self, string: str, leniency: int=10, strictness: float=0.8, tagGroupIDs: list[str]=list(linguisticTagGroups.keys())) -> None:
		self.string = string
		self.sentences = sent_tokenize(string)
		self.words = word_tokenize(string)
		self.pos = pos_tag(self.words)
		self.negativity, self.negatives, self.neutrality, self.positivity, self.positives, self.compound = sentiment(string)
		self.objects = [entity.ListProperty(linguisticTagGroups[tgid] >> self.pos, leniency=leniency, strictness=strictness) for tgid in tagGroupIDs]
		entity.Entity.__init__(self,
			entity.ListProperty(self.sentences, leniency=leniency, strictness=strictness),
			entity.ListProperty(self.words, leniency=leniency, strictness=strictness),
			entity.ListProperty(self.pos, leniency=leniency, strictness=strictness),
			entity.ListProperty(self.negatives, leniency=leniency, strictness=strictness),
			entity.ListProperty(self.positives, leniency=leniency, strictness=strictness),
			entity.MetalistProperty(self.objects, leniency=leniency, strictness=strictness),
			entity.IntProperty(self.negativity, leniency=leniency, strictness=strictness),
			entity.IntProperty(self.positivity, leniency=leniency, strictness=strictness),
			entity.IntProperty(self.compound, leniency=leniency, strictness=strictness),
		)

	def __repr__(self) -> str:
		return "<seraph.language.Tokenization of \"" + str(self) + "\">"
	
	def __str__(self) -> str:
		return self.string
	
def tokenize(string: str, leniency: int=10, strictness: float=0.8, tagGroupIDs: list[str]=list(linguisticTagGroups.keys())):
	return Tokenization(string, leniency, strictness, tagGroupIDs)

def optimize(string: str, mode: NEGATIVITY or NEUTRALITY or POSITIVITY) -> str:
