import math
import warnings

from seraph import utils
from seraph import dataset 
from seraph.common import *

delta = lambda leniency: lambda a, b: math.e ** (-1 * math.pi * (((a - b) / leniency) ** 2))
def mean(*data: list[int]) -> int:
    if len(data) == 1 and type(data[0]) == list:
        data = data[0]

    return sum(data) / len(data)

def standardDeviation():
    pass

class Differentiable:
    def difference(self, other: object) -> int:
        return 1 / self.similarity(object)

    def __matmul__(self, other: object) -> int:
        return self.difference(object)

class Property(utils.Summarizable, utils.Manufacturable, Differentiable):
    isProperty = True
    intEnabled = False
    strEnabled = False
    iterationEnabled = False
    keyingEnabled = False
    lenEnabled = False

    def __init__(self, value: any, leniency: int=10, strictness: int=.8) -> None:
        self.value = value
        self.leniency = leniency
        self.strictness = strictness

    def __repr__(self) -> str:
        return "<seraph.Property: " + repr(self.value) + ">"

    def __mod__(self, other: object) -> int:
        return self.similarity(other)

    def __len__(self) -> int:
        if not self.lenEnabled:
            raise SyntaxError("Cannot get length - did you check the type of Property you're using?")
        return len(self.value)

    def __str__(self) -> str:
        if not self.strEnabled:
            raise SyntaxError("Cannot convert to str - did you check the type of Property you're using?")
        return str(self.value)

    def __int__(self) -> int:
        if not self.intEnabled:
            raise SyntaxError("Cannot convert to int - did you check the type of Property you're using?")
        return int(self.value)

    def __iter__(self) -> object:
        if not self.iterationEnabled:
            raise SyntaxError("Cannot iterate - did you check the type of Property you're using?")
        self.n = -1
        return self

    def __next__(self) -> any:
        self.n += 1
        if self.n >= len(self.value):
            raise StopIteration
        return self.value[n]

    def __getitem__(self, index: any) -> any:
        if not self.keyingEnabled:
            raise SyntaxError("Cannot index or key - did you check the type of Property you're using?")
        return self.value[index]

    def __eq__(self, other: object) -> bool:
        if other.isProperty:
            return self % other >= self.strictness
        return self.value == other

    def summary(self) -> str:
        return "Property of class type \"" + self.__name__ + "\" and data type \"" + type(self.value).__name__ + "\": " + repr(self.value)

    def similarity(self, other: object) -> int or float:
        raise TypeError("Cannot perform similarity operation using base Propery class.")

    @staticmethod
    def make(value: any, leniency: int=10, strictness: int=.8) -> object:
        if type(value) == int:
            return IntProperty(value, leniency, strictness)
        elif type(value) == str:
            return StrProperty(value, leniency, strictness)
        elif type(value) == list:
            if issubclass(type(value[0]), Property) or type(value[0]) == Property:
                return MetalistProperty(value, leniency, strictness)
            return ListProperty(value, leniency, strictness)
        raise TypeError("Unsupported value for creation of Property: " + str(type(value).__name__) + ".")

class IntProperty(Property):
    intEnabled = True

    def similarity(self, other: Property) -> int or float:
        return delta(self.leniency)(int(self), int(other))

class StrProperty(Property):
    strEnabled = True
    lenEnabled = True

    def similarity(self, other: Property) -> int or float:
        shared = [x for x in str(self) if x in str(other)]
        diff = (len(self) - len(shared)) + abs((len(self) - len(other)))
        return delta(self.leniency)(0, diff)

class ListProperty(Property):
    iterationEnabled = True
    lenEnabled = True
    keyingEnabled = True

    def similarity(self, other: Property) -> int or float:
        return delta(self.leniency)(len(self), len(other))

class MetalistProperty(Property):
    iterationEnabled = True
    lenEnabled = True
    keyingEnabled = True

    def similarity(self, other: Property) -> int or float:
        return sum([self[index] % other[index] for index in range(len(self))])

class Entity(utils.Summarizable, utils.Makeable, Differentiable):
    def __init__(self, 
            *properties: list[Property], 
            strictness: int=.8) -> None:
        self.properties = properties
        self.strictness = strictness

    def __repr__(self) -> str:
        return "<seraph.Entity with " + str(len(self)) + " properties: " + "; ".join([repr(prop) for prop in self])[:-2] + ">"

    def __len__(self) -> int:
        return len(self.properties)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Property:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self[self.n]

    def __getitem__(self, *identifiers: int or object) -> Property or list[Property]:
        if type(identifiers[0]) == int:
            return self.properties[identifiers[0]]
        return [prop for prop in self if type(prop) in identifiers]

    def __eq__(self, other: object) -> bool:
        return self % other >= self.strictness

    def __mod__(self, other: object) -> int or float:
        return self.similarity(other)

    def similarity(self, other: object) -> int:
        return sum([a % b for a, b in zip(self, other)])

class Classifier(utils.Summarizable, utils.Makeable):
    def __init__(self, *entities: list[Entity], strictness: int=.8, selfImprove: bool=False) -> None:
        self.entities = list(entities)
        self.strictness = strictness
        self.selfImprove = selfImprove

    def __repr__(self) -> str:
        return "<seraph.Classifier of length " + str(len(self)) + ">"
    
    def __len__(self) -> int:
        return len(self.entities)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Entity:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.entities[self.n]

    def __getitem__(self, identifier: int or object) -> object:
        if type(identifier) == int:
            return self.entities[identifier]
        elif type(identifier) == Entity:
            return self.mostSimilarEntity(identifier)

    def __contains__(self, entity: Entity) -> bool:
        output = self % entity >= self.strictness
        if output and self.selfImprove:
            self += entity
        return output

    def __mod__(self, entity: Entity) -> int:
        return self.similarity(entity)

    def __iadd__(self, entity: Entity or list[Entity]) -> None:
        if type(entity) == list:
            for ent in entity:
                self += ent
        else:
            self.entities.append(entity)

    def contains(self, entity: Entity) -> bool:
        return entity in self.entities

    def similarity(self, entity: Entity) -> int:
        return sum([ent % entity for ent in self])

    def entitiesBySimilarity(self, entity: Entity) -> dict[int or float: Entity]:
        output = {}
        for ent in self:
            output[ent % entity] = ent
        return output

    def similaritiesByEntity(self, entity: Entity) -> dict[Entity: int or float]:
        output = {}
        for ent in self:
            output[ent] = ent % entity
        return output

    def mostSimilarEntity(self, entity: Entity) -> tuple[int or float, Entity]:
        ebs = self.entitiesBySimilarity(entity)
        maximum = max(ebs.keys())
        return maximum, ebs[maximum]

    def highestSimilarity(self, entity: Entity) -> Entity:
        ebs = self.entitiesBySimilarity(entity)
        return max(ebs.keys())

class HeuristicDataMap(Classifier):
    def __init__(self, data: dict[Entity: any], strictness: int=.8, selfImprove: bool=False) -> None:
        Classifier.__init__(self, *list(data.keys()), strictness=strictness, selfImprove=selfImprove)
        self.data = data

    def __repr__(self) -> str:
        return "<seraph.HeuristicDataMap of length " + str(len(self)) + ">"
    
    def __rshift__(self, entity: Entity) -> any:
        if entity in self:
            sim, mse = self.mostSimilarEntity(entity)
            return self.data[mse]
        return None
    
    def __lshift__(self, entity: Entity) -> any:
        if entity not in self:
            self += entity
            return True
        return False

class HeuristicFunctionMap(Classifier):
    def __init__(self, data: dict[Entity: any], strictness: int=.8, selfImprove: bool=False) -> None:
        Classifier.__init__(self, *list(data.keys()), strictness=strictness, selfImprove=selfImprove)
        self.data = data

    def __repr__(self) -> str:
        return "<seraph.HeuristicDataMap of length " + str(len(self)) + ">"
    
    def __rshift__(self, entity: Entity) -> any:
        if entity in self:
            sim, mse = self.mostSimilarEntity(entity)
            return self.data[mse]()
        return None
    
    def __lshift__(self, entity: Entity) -> any:
        if entity not in self:
            self += entity
            return True
        return False
    
class Aggregator:
    def __init__(self, *initials: list[list[Entity] or tuple[Entity] or Classifier], strictness: int=0.5, selfImprove: bool=False) -> None:
        self.classifiers = []
        for initial in initials:
            if type(initial) in [list, tuple]:
                self.classifiers.append(Classifier(*list(initial), strictness=strictness, selfImprove=selfImprove))
            elif type(initial) == Classifier:
                initial.strictness = strictness
                initial.selfImprove = selfImprove
                self.classifiers.append(initial)

        self.strictness = strictness
        self.selfImprove = selfImprove

    def __repr__(self) -> str:
        return "<seraph.Aggregator of length " + str(len(self)) + ">"
    
    def __len__(self) -> str:
        return len(self.classifiers)
    
    def __iter__(self) -> object:
        self.n = -1
        return self
    
    def __next__(self) -> Classifier:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.classifiers[n]
    
    def __iadd__(self, classifier: Classifier) -> None:
        self.classifiers.append(classifier)
    
    def __rshift__(self, entity: Entity) -> tuple[int or float, Entity]:
        """
        Map from the Aggregator to the Entity - in other words,
        find which entity in the whole Aggregator is most similar
        to the input.
        """
        outputs = {}
        for classifier in self:
            maximum, ent = classifier.mostSimilarEntity(entity)
            outputs[maximum] = ent
        maxkey = maximum(outputs.keys())
        return maxkey, outputs[maxkey]
    
    def __lshift__(self, entity: Entity) -> tuple[int or float, Classifier]:
        """
        Map from the Entity to the Aggregator - in other words,
        try to match the Entity with its respective Classifier 
        that is inside the Aggregator, or make a new one need be.
        """
        for classifier in self:
            if entity in classifier:
                classifier += entity
                return classifier % entity, classifier
        newClassifier = Classifier(entity, self.strictness, self.selfImprove)
        self += newClassifier
        return newClassifier
    
    def __invert__(self) -> list[Classifier]:
        return list(self)
    
    def dump(self) -> list[Classifier]:
        return ~self