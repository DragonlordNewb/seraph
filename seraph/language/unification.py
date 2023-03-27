from seraph import entity as _entity
from seraph import reaction as _reaction
from seraph import utils

class Asset(utils.Makeable):
    requirements = []

    def __init__(self, **entities: dict[str: _entity.Entity]) -> None:
        self.keys = entities.keys()
        
        for requirement in self.requirements:
            assert requirement in self.keys, "Must include " + requirement + " in " + self.__name__ + " instantiation."

        self.values = entities.values()
        self.entities = entities

    def __repr__(self) -> str:
        return "<seraph.unification.Asset of length " + str(len(self)) + ">"

    def __len__(self) -> int:
        return len(self.keys)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> tuple[str, _entity.Entity]:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return (self.keys[self.n], self.values[self.n])

    def __getitem__(self, key: str) -> _entity.Entity:
        if key not in self.keys:
            return self.__missing__(key)
        return self.entities[key]

    def __missing__(self, key) -> _entity.Entity:
        raise SyntaxError("bruh")

    def __contains__(self, other: _entity.Entity) -> bool:
        return other in self.keys or other in self.values

    def __mod__(self, other: object) -> int or float:
        sk = [key for key in self.keys if key in other.keys]
        ok = [key for key in other.keys if key in self.keys]
        return sum([1 for key1, key2 in zip(sk, ok) if self.entities[key1] == other.entities[key2]])

    def __eq__(self, other: object) -> bool:
        if len(self) != len(other):
            return False
        for key, value in self:
            if not (other[key] == value):
                return False
        return True

    def __lshift__(self, other: dict[str: _entity.Entity]) -> None:
        for key, value in zip(other.keys(), other.values()):
            if key not in self:
                self.keys.append(key)
                self.values.append(value)
                self.entities[key] = value
            
        self.entites.update(other)

    @staticmethod
    def formulateSubasset(parent: object, name: str, newRequirements: list[str], override: bool=True) -> object:
        if override:
            reqs = newRequirements
        else:
            reqs = []
            for item in self.requirements:
                reqs.append(item)
            for item in newRequirements:
                reqs.append(item)

        class Subasset(type(self)):
            __name__ = __qualname__ = name
            requirements = reqs

        return Subasset

Object = Asset.formulateSubasset(Asset, "Object", ["name"], True) # existence (really just some data points)
Location = Asset.formulateSubasset(Object, "Location", ["latitude", "longitude", "contains"], False) # space (really just a set of axes)
Event = Asset.formulateSubasset(Asset, "Event", ["epoch", "location", "participants", "actions"], True) # time (really just another axis)
Action = Event.formulateSubasset(Event, "Action", ["epoch", "location", "actor", "action", "actee"], True)

class Metric:
    def __repr__(self) -> str:
        return "<seraph.unification.Metric>"

    def __str__(self) -> str:
        return repr(self)

    def __invert__(self) -> utils.function:
        return self.distance

    def distance(self, loc1: object, loc2: object) -> int or float:
        raise SyntaxError

class EuclideanMetric:
    def distance(self, loc1: object, loc2: object):
        return None

class Space:
    def __init__(self, metric: Metric) -> None:
        self.locations = []
        self.metric = metric()

    def __repr__(self) -> str:
        return "<seraph.unification.Space with " + str(len(self)) + " locations>"

    def __len__(self) -> int:
        return len(self.locations)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> 