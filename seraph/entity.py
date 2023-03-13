import math

from seraph import utils

normal = lambda leniency: lambda x: math.e ** (-1 * math.pi * ((x / leniency) ** 2))

class Property(utils.Summarizable, utils.Makeable):
    def __init__(self, value: any) -> None:
        self.value = value

    def __repr__(self) -> str:
        return "<seraph.Property: " + repr(self.value) + ">"

    def __mod__(self, other: object) -> int:
        return self.similarity(other)

    def summary(self) -> str:
        return "Property of class type \"" + self.__name__ + "\" and data type \"" + type(self.value).__name__ + "\": " + repr(self.value)

    def similarity(self, other: object) -> int:
        raise TypeError("Cannot perform similarity operation using base Propery class.")