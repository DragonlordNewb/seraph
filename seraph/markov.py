import random

def reprPercent(percent: float) -> str:
    return str(100 * round(percent, 4)) + "%"

def fractionate(*inputs: list[float or int]):
    s = sum(inputs)
    return [x / s for x in inputs]

class MarkovLink:
    def __init__(self, id: str, **links: dict[str: any]) -> None:
        self.id = id
        self.names, self.links = links.keys(), links.values()

        self.parent = None

    def __repr__(self) -> str:
        return "<seraph.markov.MarkovLink>"

    def __len__(self) -> int:
        return len(self.names)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> tuple[str, float]:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return (self.names[self.n], self.links[self.n])

    def __eq__(self, other: str or object) -> bool:
        return self.id == other.id

class EvaluationMarkovLink(MarkovLink):
    def evaluate(self):
        for name, link in self:
            if link():
                return name
        return self.id

class StochasticMarkovLink(MarkovLink):
    def evaluate(self):
        output = random.choices(self.names, self.links)
        return output

class MarkovChain:
    def __init__(self, *links: list[MarkovLink]) -> None:
        self.links = links
        self.currentState = self.links[0]

        for link in self:
            link.parent = self

    def __repr__(self) -> str:
        "<seraph.markov.MarkovChain containing " + str(len(self)) + " links>"

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
            if type(nxt) == str:
                nxt = self[nxt]
            output.append(nxt)
            self.currentState = nxt
            n -= 1
        return output