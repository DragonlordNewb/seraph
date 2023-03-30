import time
from typing import Union

from seraph import entity as _entity
from seraph import precog

class PointInTime:
    def __init__(self, parent: object, epoch: int or float) -> None:
        self.parent = parent
        self.epoch = epoch
        self.events = []

    def __repr__(self) -> str:
        return "<seraph.unification.PointInTime " + str(self.epoch) + ">"

    def __len__(self) -> int:
        return len(self.events)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> object:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.events[self.n]

    def __contains__(self, evt: object) -> bool:
        return evt in self.events

    def __add__(self, value: int or float) -> object:
        return PointInTime(self.parent, self.epoch + value)

    def __iadd__(self, value: int or float) -> None:
        self.epoch += value

    def __invert__(self) -> _entity.Entity:
        return _entity.Entity(*[evt for evt in self])

class Event(_entity.Entity):
    def __init__(self, 
        *properties: list[_entity.Entity], 
        strictness: int=0.8,
        point: PointInTime or None=None) -> None:
        self.point = point
        _entity.Entity.__init__(self, *properties, strictness=strictness)

    def bind(self, point: PointInTime) -> None:
        self.point = point
        if self not in self.point:
            self.point.events.append(self)

    def locationInTime(self):
        return self.point.epoch

class Timeline:
    def __init__(self, epoch: Union[int, float]) -> None:
        self.epoch = epoch
        if self.epoch < time.time():
            raise RuntimeError("Timeline epoch has not yet occurred.")
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

    def __getitem__(self) -> tuple[PointInTime, list[Event]] or list[tuple[PointInTime, list[Event]]]:
        if type(indicator) == int:
            point = self.points[indicator]
            return point, [evt for evt in point]

        elif type(indicator) == Event:
            return [self[index] for index in range(len(self)) if indicator in self.points[index]]

        else:
            raise TypeError

    def __lshift__(self, pt: PointInTime) -> None:
        self.points.append(pt)

    def __rshift__(self, strictness: float=0.25) -> list[tuple[precog.Pattern, float]]:
        pre = precog.PatternRecognitionEngine()
        for pt in self:
            pre << ~pt
        return pre >> strictness

    def __add__(self, other: object) -> object:
        if self.epoch > other.epoch:
            return other + self
        timeline = Timeline(epoch=self.epoch)
        delta = other.epoch - self.epoch
        for pt, evts in other:
            pt += delta
        
        for pt, evts in self:
            timeline << pt
        for pt, evts in other:
            timeline << pt

        return timeline