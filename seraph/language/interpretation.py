from nltk import chunk
from nltk.corpus import wordnet

from seraph.language import tokenization

BRANCH = "branch"

class SyntaxTree:
    def __init__(self, *sequence: list[tuple[str, str] or object]) -> None:
        self.sequence = sequence

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

