import math

from seraph import entity

class PointProperty(entity.Property):
    iterationEnabled = True

    def similarity(self, other):
        d = math.sqrt(sum([(x2 - x1) ** 2 for x1, x2 in zip(self, other)]))
        return 2 / (1 + math.exp(d))

class PointEntity(entity.Entity):
    def __init__(self, *coordinates: list[int], strictness: int=0.8) -> None:
        entity.Entity.__init__(self, PointProperty(coordinates, strictness=strictness), strictness=strictness)

class ExpandedPointEntity(entity.Entity):
    def __init__(self, *coordinates: list[int], strictness: int=0.8) -> None:
        entity.Entity.__init__(self, [entity.IntProperty(coordinate, strictness=strictness) for coordinate in coordinates])