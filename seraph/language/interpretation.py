from nltk import word_tokenize
from nltk import pos_tag
from nltk import chunk
from nltk import tree
from nltk.corpus import wordnet

from seraph.language import tokenization

BRANCH = "branch"

class SyntaxTree:
    def __init__(self, label: str, *sequence: list[tuple[str, str] or object]) -> None:
        self.sequence = list(sequence)
        self.label = label

    def __repr__(self) -> str:
        return "<seraph.language.interpretation.SyntaxTree of length " + str(len(self)) + ">"

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

    def __iadd__(self, other) -> None:
        self.

def makeSyntaxTree(string: str, label: str="S") -> SyntaxTree:
    words = word_tokenize(string)
    pos = pos_tag(words)
    tree = chunk.ne_chunk(pos) # may take a sec

    final = SyntaxTree(label)
    for item in tree:
        if type(item) == tree.Tree:
            final += makeSyntaxTree(list(item), item.label())
        else:
            final += item

    return final