from seraph import entity as _entity
from seraph import utils

class Asset:
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

    def __eq__(self, other: object) -> bool:
        if len(self) != len(other):
            return False
        for key, value in self:
            if not ( other[key] == value):
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
    def formulateSubasset(name: str, reqs: list[str]) -> object:
        class Subasset(Asset):
            __name__ = name
            requirements = reqs

        return Subasset

Object = Asset.formulateSubasset("Object", []) # existence (really just some data points)
Location = Asset.formulateSubasset("Location", ["latitude", "longitude", "contains"]) # space (really just a set of axes)
Event = Asset.formulateSubasset("Event", ["epoch", "location", "participants", "actions"]) # time (really just another axis)

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