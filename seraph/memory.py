from seraph import entity as _entity
from seraph import reaction as _reaction
from seraph import unification

class Memory(unification.Asset):
    clarity = 0

    def __repr__(self) -> str:
        return "<seraph.memory.Memory of with clarity " + str(~self) + ">"

    def __mod__(self, other: object) -> int or float:
        sk = [key for key in self.keys if key in other.keys]
        ok = [key for key in other.keys if key in self.keys]
        return (2 ** ~self) * (2 ** ~other) * sum([1 for key1, key2 in zip(sk, ok) if self.entities[key1] == other.entities[key2]])

    def __invert__(self) -> int or float:
        return self.clarity

class MemoryFile:
    def __init__(self, *memories: list[Memory]) -> None:
        self.memories = list(memories)
        self.clarity = sum([~mem for mem in self])

    def __repr__(self) -> str:
        if len(self) > 10:
            return "<seraph.memory.MemoryFile of length " + str(len(self)) + " (too many to display)>"
        return "<seraph.memory.MemoryFile containing " + ", ".join([repr(mem) for mem in self]) + ">"

    def __len__(self) -> int:
        return len(self.memories)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Memory:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.memories[self.n]

class MemoryDrive:
    def __init__(self) -> None:
        self.files = []