import random

def reprPercent(percent: float) -> str:
    return str(100 * round(percent, 4)) + "%"

def fractionate(*inputs: list[float or int]):
    s = sum(inputs)
    return [x / s for x in inputs]

class MarkovLink:
    def __init__(self, **links: dict[str: float]) -> None:
        self.names, self.probabilities = links.keys(), links.values()

        if sum(self.probabilities) not in [1, 1.0]:
            self.probabilities = fractionate(self.probabilities)

        assert len(list(set([type(probability) for probability in self.probabilities]))) == 1, "Probabilities must all be of the same type (float)."

        self.parent = None

    def __repr__(self) -> str:
        return "<seraph.markov.MarkovLink mapping " + ", ".join([name + " with " + reprPercent(probability) + " probability" for name, probability in self]) + ">"

    def __len__(self) -> int:
        return len(self.names)

    def evaluate(self):
        output = random.choices(self.names, self.probability)
        if self.parent:
            return self.parent[output]
        return output