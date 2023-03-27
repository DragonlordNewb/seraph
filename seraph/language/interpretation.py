from nltk import word_tokenize
from nltk import pos_tag
from nltk import chunk
from nltk import tree
from nltk.corpus import wordnet

from seraph.language import tokenization
from seraph import utils

BRANCH = "branch"

class SyntaxTree:
	def __init__(self, label: str, *sequence: list[tuple[str, str] or object]) -> None:
		self.sequence = list(sequence)
		self.label = label

	def __repr__(self) -> str:
		return "<seraph.language.interpretation.SyntaxTree \"" + str(self) + "\", label=" + str(self.label) + ">"

	def __str__(self) -> str:
		return " ".join(tokenization.reform(self.sequence))

	def __len__(self) -> int:
		return len(self.sequence)

	def __iter__(self) -> object:
		self.n = -1
		return self

	def __next__(self) -> tuple[str, str] or object:
		self.n += 1
		if self.n >= len(self):
			raise StopIteration
		nxt = self.sequence[self.n]

		if type(nxt) == SyntaxTree:
			return (nxt, BRANCH)
		return nxt

	def __lshift__(self, other: str or object) -> None:
		self.sequence.append(other)

	def __rshift__(self, label: str) -> list[object]:
		found = []

		if self.label == label:
			found.append(self)

		for item, itemtype in self:
			if itemtype == BRANCH:
				if item.label == label:
					found.append(item)
				
				for recursed in item >> label:
					found.append(recursed)

		return list(set(found)) # remove list duplicates

def makeSyntaxTree(string: str, label: str="S", verbose: bool=False) -> SyntaxTree:
	if verbose: 
		print("Analyzing \"" + string + "\" ...")
	with utils.Indent():
		if verbose: 
			print("Tokenizing by words ...", end="")
		words = word_tokenize(string)
		if verbose: 
			print("done.\nTokenizing parts of speech using perceptron tagger ...", end="")
		pos = pos_tag(words)
		if verbose: 
			print("done.")
		if verbose: 
			with utils.Ellipsis("Performing chunking"):
				tr = chunk.ne_chunk(pos) # may take a sec
		else:
			tr = chunk.ne_chunk(pos)

	if verbose:
		print("Tokenization complete, parsing tree ...")
	final = SyntaxTree(label)

	first = True

	with utils.Indent():
		for item in tr:
			if type(item) == tree.Tree:
				if not first:
					if verbose: 
						print("Reached branch, parsing ...")
					final << makeSyntaxTree(tokenization.reform(list(item)), item.label())
				else:
					if verbose: 
						print("Reached unitary branch, parsing ...")
					final.label = item.label()
					for x in item:
						final << x
			else:
				if verbose: 
					print("Adding " + str(item) + " ...")
				final << item

			if first:
				first = False

	return final

def search(string: str, label: str) -> list[SyntaxTree]:
	return makeSyntaxTree(string) >> label