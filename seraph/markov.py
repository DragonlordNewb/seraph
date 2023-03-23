import random

def reprPercent(percent: float) -> str:
    return str(100 * round(percent, 4)) + "%"

def fractionate(*inputs: list[float or int]):
    s = sum(inputs)
    return [x / s for x in inputs]

class MarkovLink:
    def __init__(self, id: str, **links: dict[str: float]) -> None:
        self.id = id
        self.names, self.probabilities = links.keys(), links.values()

        if sum(self.probabilities) not in [1, 1.0]:
            self.probabilities = fractionate(self.probabilities)

        assert len(list(set([type(probability) for probability in self.probabilities]))) == 1, "Probabilities must all be of the same type (float)."

        self.parent = None

    def __repr__(self) -> str:
        return "<seraph.markov.MarkovLink mapping " + ", ".join([name + " with " + reprPercent(probability) + " probability" for name, probability in self]) + ">"

    def __len__(self) -> int:
        return len(self.names)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> tuple[str, float]:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return (self.names[self.n], self.probabilities[self.n])

    def __eq__(self, other: str or object) -> bool:
        return self.id == other.id

    def evaluate(self):
        output = random.choices(self.names, self.probability)
        if self.parent:
            return self.parent[output]
        return output

class MarkovChain:
    def __init__(self, *links: list[MarkovLink]) -> None:
        self.links = links
        self.currentState = self.links[0]

        for link in self:
            link.parent = self

    def __repr__(self) -> str:
        "<seraph.markov.MarkovChain containing " + ", ".join([repr(link) for link in self]) + ">"

    def __len__(self) -> int:
        return len(self.links)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> MarkovLink:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.links[self.n]

    def __getitem__(self, id: str) -> MarkovLink:
        for link in self:
            if link == id:
                return link
        raise KeyError

    def evaluate(self, n: int=1) -> list[MarkovLink]:
        output = []
        while n > 0:
            nxt = self.currentState.evaluate()
            output.append(nxt)
            self.currentState = nxt
            n -= 1
        return output