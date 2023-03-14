import math

from seraph import utils

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

class Property(utils.Summarizable, utils.Makeable, Differentiable):
    isProperty = True
    intEnabled = False
    strEnabled = False
    iterationEnabled = False
    keyingEnabled = False
    lenEnabled = False

    def __init__(self, value: any, leniency: int=1, strictness: int=1) -> None:
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

    def similarity(self, other: object) -> int:
        raise TypeError("Cannot perform similarity operation using base Propery class.")

class IntProperty(Property):
    intEnabled = True

    def similarity(self, other: Property) -> int:
        return normal(self.leniency)(int(self), int(other))

class StrProperty(Property):
    strEnabled = True
    lenEnabled = True

    def similarity(self, other: Property) -> int:
        shared = [x for x in str(self) if x in str(other)]
        diff = (len(self) - len(shared)) + abs((len(self) - len(other)))
        return normal(self.leniency)(0, diff)

class ListProperty(Property):
    iterationEnabled = True
    lenEnabled = True
    keyingEnabled = True

    def similarity(self, other: Property):
        return normal(self.leniency)(len(self), len(other))

class MetalistProperty(Property):
    iterationEnabled = True
    lenEnabled = True
    keyingEnabled = True

    def similarity(self, other: Property) -> int:
        return sum([self[index] % other[index] for index in range(len(self))])

class Entity(utils.Summarizable, utils.Makeable, Differentiable):
    def __init__(self, 
            *properties: list[Property], 
            strictness: int=1) -> None:
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
        if type(identifier[0]) == int:
            return self.properties[identifier[0]]
        return [prop for prop in self if type(prop) in identifiers]

    def __mod__(self, other: object) -> int:
        return self.similarity(other)

    def similarity(self, other: object) -> int:
        return sum([a % b for a, b in zip(self, other)])

class Classifier(utils.Summarizable, utils.Makeable):
    def __init__(self, *entities: list[Entity], strictness: int=1, selfImprove: bool=False) -> None:
        self.entities = entities
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

    def entitiesBySimilarity(self, entity: Entity) -> dict[int: Entity]:
        output = {}
        for ent in self:
            output[ent % entity] = ent
        return output

    def similaritiesByEntity(self, entity: Entity) -> dict[Entity: int]:
        output = {}
        for ent in self:
            output[ent] = ent % entity
        return output

    def mostSimilarEntity(self, entity: Entity) -> Entity:
        ebs = self.entitiesBySimilarity(entity)
        maximum = max(ebs.keys())
        return ebs[maximum]

    def highestSimilarity(self, entity: Entity) -> Entity:
        ebs = self.entitiesBySimilarity(entity)
        return max(ebs.keys())