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

NEGATIVITY = NEGATIVE = "negativity"
NEUTRALITY = NEUTRAL = "neutrality"
POSITIVITY = POSITIVE = "positivity"

def reprReview(s):
	if s == NEGATIVITY:
		return "negative"
	if s == NEUTRALITY:
		return "neutral"
	return "positive"

def lemmas(string: str) -> list[object]:
	output = []
	for ss in wordnet.synsets(string):
		for lemma in ss.lemmas():
			output.append(lemma.name())
	return output

def synonyms(string: str, depth: int=1) -> list[str]:
	output = [string]
	for iteration in range(depth):
		newOutput = [x for x in output]
		for word in output:
			for synset in wordnet.synsets(word):
				newOutput.append(synset.name().split(".")[0])
		output = list(set(newOutput))
	return output

def wordSentiment(string: str, depth: int=0) -> tuple[float, POSITIVE or NEGATIVE or NEUTRAL, list[tuple[str, int]]]:
    wordlist = [(string, 1)]
    for iteration in range(depth):
        for word in wordlist:
            for synonym in synonyms(word):
                if synonym not in wordlist:
                    wordlist.append((synonym, iteration))

    sentiment = 0
    for word, inverseWeight in wordlist:
        sentiment += 1 / inverseWeight

    if sentiment > 1:
        indicator = POSITIVE
    elif sentiment < 1:
        indicator = NEGATIVE
    else:
        indicator = NEUTRAL

    return (sentiment, indicator, wordlist)  

sid = vader.SentimentIntensityAnalyzer()

def sentiment(string: str) -> tuple[float, list[str], float, float, list[str], float]:
	"""
	Use the VADER sentiment analysis tool to analyze a sentence.
	Returns a sextuple of the negativity of the sentence, negative words in the sentence, the
	neutrality of the sentence, the positivity of the sentence, positive words in the sentence,
	and the modification by compounding, all as floats or lists of strings where applicable.
	"""
	global sid

	result = sid.polarity_scores(string)
	tk = word_tokenize(string)
	return (
        result["neg"],
        [s for s in tk if s in opinion_lexicon.negative()], 
        result["neu"], 
        [s for s in tk if not (s in opinion_lexicon.negative() or s in opinion_lexicon.positive())],
        result["pos"], 
        [s for s in tk if s in opinion_lexicon.positive()], 
        result["compound"]
    )

class SentimentAnalysis:
	def __init__(self, string: str, threshold: float=0.25):
		self.negativity, self.negatives, self.neutrality, self.neutrals, self.positivity, self.positives, self.compound = sentiment(string)
		self.overall = NEUTRAL
		if self.compound > threshold:
			self.overall = POSITIVE
		if self.compound < -1 * threshold:
			self.overall = NEGATIVE
		self.string = string
		self.words = word_tokenize(self.string)

	def __repr__(self) -> str:
		return "<seraph.language.SentimentAnalysis of \"" + str(self) + "\", overall sentiment: " + reprReview(self.overall) + ">"

	def __str__(self) -> str:
		return self.string

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
		self.negativity, self.negatives, self.neutrality, self.neutrals, self.positivity, self.positives, self.compound = sentiment(string)
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

class Sentence:
    def __init__(self, string: str) -> None:
        self.tok = tokenize(string)
        self.words = word_tokenize(string)
        self.pointer = 0
        self.negativity, self.negatives, self.neutrality, self.neutrals, self.positivity, self.positives, self.compound = sentiment(str(self))

    def __repr__(self) -> str:
        return "<seraph.language.Sentence \"" + str(self) + "\">"

    def __str__(self) -> str:
        return " ".join(self.words)

    def __len__(self) -> int:
        return len(self.words)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> str:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.words[self.n]

    def __getitem__(self, index: int) -> object:
        self.pointer = index
        return self

    def __lshift__(self, replacement: str) -> None:
        self.words[self.pointer] = replacement
        self.tok = tokenize(str(self))
        self.pointer = 0
        self.negativity, self.negatives, self.neutrality, self.neutrals, self.positivity, self.positives, self.compound = sentiment(str(self))

def optimize(string: str or Sentence, mode: NEGATIVITY or NEUTRALITY or POSITIVITY or float or int, maximumDepth: int=100) -> str:
    # probably one of the most overloaded functions i've written yet, lol

    original = string

    if type(mode) in [int, float]:
        if mode < 0:
            optimization = NEGATIVITY
        elif mode > 0:
            optimization = POSITIVITY
        else:
            optimization = NEUTRALITY

        for depth in range(maximumDepth):
            negativity, negatives, neutrality, neutrals, positivity, positives, compound = sentiment(string)

            general = negativity + positivity

            if general > 0:
                pass