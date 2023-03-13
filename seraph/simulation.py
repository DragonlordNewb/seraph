# THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE
# PUBLIC LICENSE ("AGREEMENT"). ANY USE, REPRODUCTION OR DISTRIBUTION
# OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT.

import math

from seraph import dataset
from seraph import utils
from seraph.common import *

class Agent(utils.Makeable):
    def __init__(self, 
            dataset: dataset.Dataset or list, 
            function: utils.function or None=None, 
            parentAgent: object or None=None, 
            parentPhylogeny: object or None=None) -> None:
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
    
    def vary(self, 
            variance: int=1, 
            indexBlacklist: list[int]=[], 
            elementBlacklist: list[dataset.Element]=[],
            forceInject: list[Element]=[], 
            ageIncrement: int=1) -> object:
        self.dataset.vary(variance, indexBlacklist, elementBlacklist, forceInject, ageIncrement)

    def generateVariants(self, 
            length: int or None=None, 
            n: int=1, variance: int=1, 
            indexBlacklist: list[int]=[], 
            elementBlacklist: list[Element]=[], 
            forceInject: list[Element]=[]) -> list[object]:
        if length == None:
            length = len(self)

        output = []
        for _ in range(n):
            agent = Agent(
                self.dataset.generateVariants(
                    length, 
                    1, 
                    variance, 
                    indexBlacklist, 
                    elementBlacklist
                )[0], 
                self.function, 
                self
            )
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

        self.scoreValue = UNKNOWN
        self.relativeScore = UNKNOWN

        self._scored = False

        self.dead = False

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

    def hasDaughters(self) -> bool:
        return len(self.daughterPhylogenies) > 0

    def hasNoDaughters(self) -> bool:
        return len(self.daughterPhylogenies) == 0

    def hasBeenScored(self) -> bool:
        return self._scored

    def siblings(self, separation: int=1) -> list[object]:
        return [phylogeny for phylogeny in self.parentPhylogeny.daughterPhylogenies if phylogeny != self]

    def score(self, n: int) -> int:
        parentScore = self.parentPhylogeny.scoreValue
        self.scoreValue = n
        self.relativeScore = self.scoreValue - self.parentPhylogeny.scoreValue
        for element in self.agent.dataset:
            element.relativeScore = self.relativeScore
        self._scored = True
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
            forceInject: list[Element]=[],
            simulation: object or None=None) -> list[object]:
        if not self.dead:
            daughters = self.agent.generateVariants(length, n, variance, indexBlacklist, elementBlacklist)
            self.assignDaughterAgents(*daughters)
            if simulation:
                for daughter in self.daughterPhylogenies:
                    if daughter.agent in daughters:
                        simulation.phylogenies.append(daughter)
            return daughters
        return []
    
    def summary(self) -> str:
        base = "Phylogeny of " + repr(self.agent)
        if len(self):
            others = []
            for daughter in self:
                others.append("  " + daughter.summary())
        base = base + "\n".join(others)
        return base

    def kill(self) -> None:
        self.dead = True

class Simulation:
    def __init__(self, 
            *foundations: list[Agent or Phylogeny], 
            expansionFactor: int=2, 
            extinctionFactor: int=2, 
            improvementFactor: int=1,
            scoringFunction: utils.function or None=None) -> None:
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

        # if unequal, can lead to exponential expansion or eventual necrosis
        self.expansionFactor = expansionFactor
        self.extinctionFactor = extinctionFactor
        self.improvementFactor = improvementFactor

        self.isConstantPopulation = self.expansionFactor == self.extinctionFactor

        self.positiveElements = []
        self.negativeElements = []

        self.forceInjectionBuffer = []

    def __len__(self) -> int:
        return len(self.phylogenies)
    
    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Phylogeny:
        self.n += 1
        if n >= len(self):
            raise StopIteration
        return self.phylogenies[n]

    def buffer(self, *forceInject: list[list[dataset.Element]]):
        for injection in forceInject:
            self.forceInjectionBuffer.append(injection)

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

    def lastGeneration(self) -> list[Phylogeny]:
        lg = [phylogeny for phylogeny in self if phylogeny.hasNoDaughters() and not phylogeny.dead]
        lg.sort(key=lambda phylogeny: phylogeny.relativeScore)
        return lg

    def scoreAll(self) -> list[int]:
        scores = []
        for phylogeny in self.lastGeneration():
            if not phylogeny.hasBeenScored():
                scores.append(self.score(phylogeny))
        return scores

    def scoreAchieved(self, score: int) -> bool, Phylogeny or None:
        for phylogeny in self:
            if phylogeny.score >= score:
                return True, phylogeny
        return False, None

    def relativeScoreAchieved(self, score: int) -> bool, Phylogeny or None:
        for phylogeny in self:
            if phylogeny.relativeScore >= score:
                return True, phylogeny
        return False, None
    
    def currentBest(self) -> Phylogeny: # make this work for any data type requested please!
        best = self.phylogenies[0]
        for phylogeny in self.phylogenies:
            if phylogeny.score > best.score:
                best = phylogeny
        return best

    def evolve(self, variance: int=1) -> None:
        if self._firstEvolution:
            for phylogeny in self:
                phylogeny.generateVariants(
                    length=None, 
                    n=self.expansionFactor, 
                    variance=variance,
                    simulation=self
                )

            self._firstEvolution = False

        else:
            lastGeneration = self.lastGeneration()

            # assert that all phylogenies have been scored
            self.scoreAll()

            # sort them by who has improved the most
            lastGeneration.sort(key=lambda phylogeny: phylogeny.relativeScore)

            # extinct the worst fraction.
            extinctionLimit = math.ceil((len(lastGeneration) - 1) / self.extinctionFactor)
            for phylogeny in lastGeneration[extinctionLimit:]:
                phylogeny.kill() # could be optimized with map()?
            # should've done better if they didn't want to die.
            # that's evolution for you.

            # identify which elements caused improvements to appear
            survivors = [phylogeny for phylogeny in lastGeneration if not phylogeny.dead]
            # resort the survivors
            survivors.sort(key=lambda phylogeny: phylogeny.relativeScore)

            for best in survivors[:self.improvementFactor]:
                parent = best.parentPhylogeny
                delta = dataset.Dataset.delta(best.agent.dataset, parent.agent.dataset)
                for element in delta:
                    self.positiveElements.append(element)

            for best in survivors[-1 * self.improvementFactor:]:
                parent = best.parentPhylogeny
                delta = dataset.Dataset.delta(best.agent.dataset, parent.agent.dataset)
                for element in delta:
                    self.negativeElements.append(element)
            
            # generate new variants
            newInjection = self.forceInjectionBuffer.pop()
            for phylogeny in lastGeneration:
                phylogeny.generateVariants(
                    length=None, 
                    n=self.expansionFactor, 
                    variance=variance,
                    elementBlacklist=self.negativeElements,
                    forceInject=newInjection,
                    simulation=self
                )

    def achieveScore(self, 
            score: int, 
            variance: int=1, 
            returnValue: None or dataset.Element or Dataset or Agent or Phylogeny=None, 
            maximum: int=1000) -> list[any] or list[dataset.Element] or Dataset or Agent or Phylogeny:
        self.scoreAll()
        for generation in range(maximum):
            self.evolve(variance)
            achieved, phylogeny = self.scoreAchieved(score)
            if achieved:
                return True, phylogeny
        return False, None

    def maximize(self, n: int=1000) -> any:
        pass