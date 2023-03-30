import time

from seraph import entity as _entity
from seraph import precog

class PointInTime:
    def __init__(self, parent: object, epoch: int or float) -> None:
        self.parent = parent
        self.epoch = epoch

    def __repr__(self) -> str:
        return "<seraph.unification.PointInTime " + str(self.epoch) + ">"

    def __add__(self, value: int or float) -> object:
        return PointInTime(self.parent, self.epoch + value)

    def __iadd__(self, value: int or float) -> None:
        self.epoch += value

class Event(_entity.Entity):
    def __init__(self, 
        *properties: list[_entity.Entity], 
        strictness: int=0.8,
        point: PointInTime or None=None) -> None:
        self.point = point
        _entity.Entity.__init__(self, *properties, strictness=strictness)

    def bind(self, point: PointInTime) -> None:
        self.point = point

class Timeline:
    def __init__(self, epoch: int or float, rate: int or float) -> None:
        self.epoch = epoch
        if self.epoch < time.time():
            raise RuntimeError("Timeline epoch has not yet occurred.")
        self.rate = rate
        self.points = []

    def __repr__(self) -> str:
        return "<seraph.unification.Timeline: " + "\n  ".join(self) + "\n(" + str(len(self)) + " points)>"

    def __len__(self) -> int:
        return len(self.points)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> PointInTime:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self[self.n]

    def __getitem__(self) -> PointInTime:
        if type(indicator) == int:
            return self.points[indicator]

        