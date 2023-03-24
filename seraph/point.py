import math

from seraph import entity

class PointProperty(entity.Property):
    iterationEnabled = True

    def similarity(self, other):
        d = math.sqrt(sum([(x2 - x1) ** 2 for x1, x2 in zip(self, other)]))
        return 2 / (1 + math.exp(d))

    def distance(self, other):
        return math.sqrt(sum([(x2 - x1) ** 2 for x1, x2 in zip(self, other)]))

class PointEntity(entity.Entity):
    def __init__(self, *coordinates: list[int], strictness: int=0.8) -> None:
        entity.Entity.__init__(self, PointProperty(coordinates, strictness=strictness), strictness=strictness)

class ExpandedPointEntity(entity.Entity):
    def __init__(self, *coordinates: list[int], strictness: int=0.8) -> None:
        self.coordinates = coordinates
        entity.Entity.__init__(self, *[entity.IntProperty(coordinate, strictness=strictness) for coordinate in coordinates])

    def __len__(self) -> int:
        return len(self.coordinates)

    def __iter__(self) -> object:
        self.n = -1
        return self
    
    def __next__(self) -> int or float:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self[self.n]

    def __getitem__(self, index: int) -> entity.IntProperty:
        return self.properties[index].value

    def __add__(self, other: object) -> object:
        assert len(self) == len(other), "Can only perform operations on Point objects with the same dimension."
        return ExpandedPointEntity(*[x1 + x2 for x1, x2 in zip(self, other)])

    def __iadd__(self, value: list[int]) -> None:
        self.translate(*value)

    def __imul__(self, value: list[int]) -> None:
        self.scale(*value)

    def translate(self, *translation) -> None:
        for index, coordinate in enumerate(translation):
            self.properties[index] += coordinate

    def scale(self, *scale) -> None:
        for index, coordinate in enumerate(scale):
            self.properties[index] *= coordinate

def midpoint(self, *points: list[ExpandedPointEntity]) -> ExpandedPointEntity:
    averages = []
    for index in range(len(points[0])):
        averages.append(sum([point[index] for point in points]) / len(points))
    return ExpandedPointEntity(*averages)