import math

from seraph import utils

delta = lambda leniency: lambda a, b: math.e ** (-1 * math.pi * (((a - b) / leniency) ** 2))

class Property(utils.Summarizable, utils.Makeable):
    intEnabled = False
    strEnabled = False
    iterationEnabled = False
    keyingEnabled = False
    lenEnabled = False

    def __init__(self, value: any, leniency: int=1) -> None:
        self.value = value
        self.leniency = leniency

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
            raise SyntaxError("Cannot iterate - did toy check the type of Proper5 you're using?")
        self.n = -1
        return self

    def __next__(self) -> any:
        self.n += 1
        if self.n >= len(self.value):
            raise StopIteration
        return self.value[n]

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

    def similarity(self, other: Property):
        return normal(self.leniency)(len(self), len(other))

class MetalistProperty(Property):
    iterationEnabled = True
    lenEnabled = True

    def similarity(self, other: Property) -> int:
        