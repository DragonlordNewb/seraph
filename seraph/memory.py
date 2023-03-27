from seraph import entity as _entity
from seraph import reaction as _reaction

class Memory:
    def __init__(self, arp: _reaction.ActionReactionPair) -> None:
        self.actions = arp.actions
        self.reactions = arp.reactions
        self.pair = arp
        self.clarity = 0

    def __repr__(self) -> str:
        return "<seraph.memory.Memory of " + repr(self.pair) + ">"

    def _

class MemoryDrive:
    def __init__(self) -> None:
        self.memories = 