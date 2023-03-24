# THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE
# PUBLIC LICENSE ("AGREEMENT"). ANY USE, REPRODUCTION OR DISTRIBUTION
# OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT.

from seraph import entity
from seraph import reaction
from seraph import utils

with utils.Indent():
	print("Importing NLTK ...", end="")
	import nltk
	from nltk.corpus import wordnet
	from nltk.corpus import framenet
	from nltk.tag import pos_tag
	from nltk.tokenize import word_tokenize
	from nltk.tokenize import sent_tokenize
	from nltk.sentiment import vader
	from nltk.corpus import opinion_lexicon
	print("done.")

class Tokenization:
