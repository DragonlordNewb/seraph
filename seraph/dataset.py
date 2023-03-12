# THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE
# PUBLIC LICENSE ("AGREEMENT"). ANY USE, REPRODUCTION OR DISTRIBUTION
# OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT.

import random

from seraph import utils

class Element(utils.Summarizable, utils.Makeable):
    def __init__(self, value: any, age: int=1) -> None:
        self.value = value
        self.age = age

    def __repr__(self) -> str:
        return "<seraph.Element " + repr(self.value) + ", age " + str(self.age) + ">"

    def __eq__(self, element):
        if type(element) == Element:
            return self.value == element.value
        else:
            return self.value == element
    
    def summary(self) -> str:
        return "Age " + str(self.age) + ": " + repr(self.value)

    def increaseAge(self, n: int=1) -> int:
        self.age += n
        return self.age

class Dataset(utils.Summarizable):
    def __init__(self, *elements: list[Element], parentDataset: object or None=None) -> None:
        self.elements = elements

        badIndices = []
        for index, element in enumerate(self.elements):
            if element is None:
                badIndices.append(index)
        self.elements = [self.elements[x] for x in range(len(self)) if x not in badIndices]
        
        self.parentDataset = parentDataset or self

        self.isFoundation = self.parentDataset == self

    def __repr__(self) -> str:
        return "<seraph.Dataset of length " + str(len(self)) + ">"

    def __len__(self) -> int:
        return len(self.elements)
    
    def __contains__(self, item: Element) -> bool:
        return item in self.elements

    def __iter__(self) -> object:
        self.n = -1
        return self
    
    def __next__(self) -> any:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.elements[self.n]
    
    def summary(self) -> str:
        output = "Dataset of length " + str(len(self)) + ":\n"
        for index, element in enumerate(self):
            output = output + "  " + str(index) + " - " + element.summary() + "\n"
        return output[:-1]
    
    def shuffle(self) -> object:
        random.shuffle(self.elements)
        return Dataset(*self.elements)
    
    def add(self, element: any) -> None:
        self.elements.append(element)

    def replaceIndex(self, index: int, element: any, ageIncrement: int=0) -> None:
        element.increaseAge(ageIncrement)
        self.elements[index] = element

    def replaceElement(self, existing: any, replaced: any, ageIncrement: int=0) -> None:
        replaced.increaseAge(ageIncrement)
        for index, element in enumerate(self):
            if element == existing:
                self.replaceIndex(index, replaced)
                break
    
    def randomIndices(self, n: int=1, blacklist: int or list[int]=[]) -> any:
        if type(blacklist) != list:
            blacklist = [blacklist]

        assert n <= len(self), "Can't get more random unique indices than there are in the Dataset."

        indices = [x for x in range(len(self)) if x not in blacklist]
        return [indices[random.randint(0, len(indices) - 1)] for _ in range(n)]
    
    def randomUniqueIndices(self, n: int=1, blacklist: int or list[int]=[]) -> any:
        if type(blacklist) != list:
            blacklist = [blacklist]

        assert n <= len(self), "Can't get more random unique indices than there are in the Dataset."

        indices = [x for x in range(len(self)) if x not in blacklist]
        return [indices.pop(random.randint(0, len(indices) - 1)) for _ in range(n)]
    
    def randomElements(self, n: int=1, blacklist: any or list[Element]=[], ageIncrement: int=0) -> list[Element]:
        if type(blacklist) != list:
            blacklist = [blacklist]

        assert n <= len(self), "Can't get more random unique indices than there are in the Dataset."

        elements = [element for element in self.elements if element not in blacklist]
        output = [elements[random.randint(0, len(elements) - 1)] for _ in range(n)]
        for element in output:
            element.increaseAge(ageIncrement)

        return output
    
    def randomUniqueElements(self, n: int=1, blacklist: any or list[Element]=[], ageIncrement: int=0) -> list[Element]:
        if type(blacklist) != list:
            blacklist = [blacklist]

        assert n <= len(self), "Can't get more random unique elements than there are in the Dataset."

        elements = [element for element in self.elements if element not in blacklist]
        output = [elements.pop(random.randint(0, len(elements) - 1)) for _ in range(n)]
        for element in output:
            element.increaseAge(ageIncrement)

        return output
    
    def vary(self, variance: int=1, indexBlacklist: list[int]=[], elementBlacklist: list[Element]=[], ageIncrement: int=1) -> object:
        indices = self.parentDataset.randomUniqueIndices(variance, indexBlacklist)
        elements = self.parentDataset.randomUniqueElements(variance, elementBlacklist)
        
        for index, element in zip(indices, elements):
            self.replaceIndex(index, element, ageIncrement)

        return self
    
    def generateVariants(self, length: int or None=None, n: int=1, variance: int=1, indexBlacklist: list[int]=[], elementBlacklist: list[Element]=[]) -> list[object]:
        if length == None:
            length = len(self)
        
        output = []
        for _ in range(n):
            variant = Dataset(*self.randomUniqueElements(length, elementBlacklist, 1), self)
            variant.vary(variance, indexBlacklist, elementBlacklist)
            output.append(variant)
        return output
    
    @classmethod
    def make(cls, *elements: list[any or Element], parentDataset: any=None) -> object:
        elems = []
        if len(elements) == 1 and type(elements) == list:
            elements = elements[0] # auto-unpack the list so that you don't need a separate function to differentiate between .make(a, b, c) and .make([a, b, c])
        for element in elements:
            if type(element) == Element:
                elems.append(element)
                continue
            elems.append(Element.make(element))
        return cls(*[x for x in elems if x != None], parentDataset)