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

class Timeline:
    def __init__(self, epoch: int or float, rate: int or float) -> None:
        self.epoch = epoch
        if self.epoch < time.time():
            raise RuntimeError("Timeline epoch has not yet occurred.")
        self.rate = rate

        

    def __repr__(self) -> str:
        return "<seraph.unification.Timeline"
