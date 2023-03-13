# THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE
# PUBLIC LICENSE ("AGREEMENT"). ANY USE, REPRODUCTION OR DISTRIBUTION
# OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT.

import random

from seraph import dataset
from seraph import utils
from seraph.common import *

class Agent(utils.Makeable):
    def __init__(self, dataset: dataset.Dataset or list, function: utils.function or None=None, parentAgent: object or None=None, parentPhylogeny: object or None=None) -> None:
        if type(dataset) == list:
            dataset = dataset.Dataset.make(dataset)

        self.dataset = dataset

        if (not hasattr(self, "function")) and (function != None):
            self.function = function
        elif hasattr(self, "function") and (function != None):
            raise SyntaxError("Cannot both subclass a \"function\" method and supply one at init.")
        elif (not hasattr(self, "function")) and (function == None):
            raise SyntaxError("Must either subclass a \"function\" method or supply one at init.")
        
        self.parentAgent = parentAgent or self

        self.isFoundation = self.parentAgent == self

        self.parentPhylogeny = parentPhylogeny

    def __repr__(self) -> str:
        return "<seraph.Agent dataset=" + repr(self.dataset) + " function=" + str(self.function) + ">"

    def __len__(self) -> int:
        return len(self.dataset)
        
    def function(self, *args: list, **kwargs: dict) -> SyntaxError:
        raise SyntaxError("Cannot call \"function\" from base Agent class.")
    
    def vary(self, variance: int=1, indexBlacklist: list[int]=[], elementBlacklist: list[dataset.Element]=[], ageIncrement: int=1) -> object:
        self.dataset.vary(variance, indexBlacklist, elementBlacklist, ageIncrement)

    def generateVariants(self, length: int or None=None, n: int=1, variance: int=1, indexBlacklist: list[int]=[], elementBlacklist: list[Element]=[]) -> list[object]:
        if length == None:
            length = len(self)

        output = []
        for _ in range(n):
            agent = Agent(self.dataset.generateVariants(length, 1, variance, indexBlacklist, elementBlacklist)[0], self.function, self)
            output.append(agent)

        if self.parentPhylogeny != None:
            self.parentPhylogeny.assignDaughterAgents(*output)

        return output
    
class Phylogeny(utils.Summarizable, utils.Makeable):
    def __init__(self, agent: Agent, parentPhylogeny: object or None=None) -> None:
        self.agent = agent
        self.parentPhylogeny = parentPhylogeny or self

        self.isFoundation = self.parentPhylogeny == self

        self.daughterPhylogenies = []

        self.score = UNKNOWN
        self.relativeScore = UNKNOWN

    def __repr__(self) -> str:
        return "<seraph.Phylogeny agent=" + str(self.agent) +  " with " + str(len(self)) + " daughter phylogenies>"
    
    def __len__(self) -> int:
        return len(self.daughterPhylogenies)
    
    def __iter__(self) -> object:
        self.n = -1
        return self
    
    def __next__(self) -> object:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.daughterPhylogenies[n]

    def score(self, n: int) -> int:
        parentScore = self.parentPhylogeny.score
        self.score = n
        self.relativeScore = self.score - self.parentPhylogeny.score
        for element in self.agent.dataset:
            element.relativeScore = self.relativeScore
        return self.relativeScore

    def assignDaughterAgents(self, *daughters: list[Agent]) -> None:
        for daughter in daughters:
            self.daughterPhylogenies.append(Phylogeny(daughter, self))

    def generateVariants(self, 
            length: int or None=None, 
            n: int=1, 
            variance: int=1, 
            indexBlacklist: list[int]=[], 
            elementBlacklist: list[Element]=[], 
            simulation: object or None=None) -> list[object]:
        daughters = self.agent.generateVariants(length, n, variance, indexBlacklist, elementBlacklist)
        self.assignDaughterAgents(*daughters)
        if simulation:
            for daughter in self.daughterPhylogenies:
                if daughter.agent in daughters:
                    simulation.phylogenies.append(daughter)
        return daughters
    
    def summary(self) -> str:
        base = "Phylogeny of " + repr(self.agent)
        if len(self):
            others = []
            for daughter in self:
                others.append("  " + daughter.summary())
        base = base + "\n".join(others)
        return base

class Simulation:
    def __init__(self, *foundations: list[Agent or Phylogeny], scoringFunction: utils.function or None=None) -> None:
        for index, item in enumerate(foundations):
            if type(item) == Agent:
                foundations[index] = Phylogeny.make(item)
            elif type(item) == Phylogeny:
                pass
            else:
                raise TypeError("Can only supply Phylogeny or Agent objects to Simulation at init.")

        self.phylogenies = foundations

        self._firstEvolution = True

        if (not hasattr(self, "scoringFunction")) and (scoringFunction != None):
            self.scoringFunction = scoringFunction
        elif hasattr(self, "scoringFunction") and (scoringFunction != None):
            raise SyntaxError("Cannot both subclass a \"scoringFunction\" method and supply one at init.")
        elif (not hasattr(self, "scoringFunction")) and (scoringFunction == None):
            raise SyntaxError("Must either subclass a \"scoringFunction\" method or supply one at init.")

    def __len__(self) -> int:
        return len(self.phylogenies)
    
    def __iter__(self) -> object:
        self.n = -1

    def __next__(self) -> Phylogeny:
        self.n += 1
        if n >= len(self):
            raise StopIteration
        return self.phylogenies[n]

    def score(self, item: Phylogeny or Agent) -> int:
        if type(item) == Phylogeny:
            s = self.scoringFunction(item.agent)
            item.score(s)
            return s
        elif type(item) == Agent:
            s = self.scoringFunction(item)
            item.parentPhylogeny.score(s)
            return s
        else:
            raise TypeError("Can only score Phylogeny or Agent objects, not " + str(item.__name__) + ".")

    def evolve(self, variance: int) -> None:
        if self._firstEvolution:
            for phylogeny in self:
                phylogeny.