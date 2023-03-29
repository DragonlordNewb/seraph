from seraph import entity as _entity

class Pattern:
    def __init__(self, *entities: list[_entity.Entity]) -> None:
        self.entities = entities

    def __repr__(self) -> str:
        return "<seraph.precog.Pattern wrapping " + ", ".join([repr(entity) for entity in self]) + ">"

    def __len__(self) -> int:
        return len(self.entities)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> _entity.Entity:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.entities[self.n]

    def __mod__(self, other: object) -> int or float:
        # ugh, here we go again

        if len(self) > len(other):
            return other % self

        elif len(self) == len(other):
            return sum([e1 % e2 for e1, e2 in zip(self, other)])

        else: 
            # implies len(self) < len(other)
            result = -1
            for offset in range(len(other) - len(self)):
                x = sum([e1 % e2 for e1, e2 in zip(self, other[offset:])])
                if x > result:
                    result = x

            return result

class PatternRecognitionEngine:
    def __init__(self) -> None:
        self.pattern = []

    def __repr__(self) -> str:
        return "<seraph.precog.PatternRecognitionEngine of length " + str(len(self)) + ">"

    def __len__(self) -> int:
        return len(self.pattern)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> _entity.Entity:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.patterns[self.n]

    def __lshift__(self, item: _entity.Entity):
        if self._checkIncompatibility(item):
            raise TypeError("Entities must be compatible to add them to the pattern.")

        self.pattern.append(item)

    def __rshift__(self, strictness: int=0.25) -> Pattern:
        patterns: list[tuple[Pattern, float]] = [] # (pattern, confidence) pairs
        for index in range(1, min(len(self), maxlength), -1):
            # assemble blocks
            blocks = []
            i = 0
            currentBlock = []
            for item in self:
                currentBlock.append(item)
                i += 1
                if i == index:
                    i = 0
                    blocks.append(currentBlock)
                    currentBlock = []

            # setup for pattern identification
            initial = blocks[0]
            blocks = blocks[:-1] # clip off the last block, it could be incomplete and isn't useful
            
            for index, block in enumerate(blocks):
                equality = 0
                for otherIndex, otherBlock in enumerate(blocks):
                    if otherIndex != index:
                        similarity = 0
                        for item1, item2 in zip(block, otherBlock):
                            equality += item1 % item2

                pattern = Pattern(*block)
                confidence = equality / (len(blocks) - 1)
                sufficient = confidence >= strictness

                patterns.append((
                    pattern,
                    confidence,
                    sufficient
                ))

        return [(pattern, confidence) for pattern, confidence, sufficient in patterns if sufficient]

    def __or__(self, pattern: Pattern) -> float:


    def __enter__(self) -> object:
        self.dump()
        return self

	def __exit__(self, exception, value, tb) -> bool or None:
		if exception is not None:
			return False

    def _checkCompatibility(self, entity: _entity.Entity) -> bool:
        if len(self) == 0:
            return True
        
        base = self.pattern[0]
        if len(base) != len(entity):
            return False
        for prop1, prop2 in zip(base, entity):
            if type(prop1) != type(prop2):
                return False

        return True

    def _checkIncompatibility(self, entity: _entity.Entity) -> bool:
        return not self._checkCompatibility(entity)

    def dump(self) -> list[_entity.Entity]:
        return [self.patterns.pop(0) for _ in range(len(self))]

    def synthesize(self, strictness: int=0.25) -> Pattern:
        return self >> strictness