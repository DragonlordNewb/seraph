from seraph import entity as _entity

class Pattern:
    def __init__(self, *entities: list[_entity.Entity]) -> None:
        self.entities = entities

class Context:
    def __init__(self, entities: list[Pattern], *patterns: list[Pattern], strictness: int=.8) -> None:
        self.entities = list(entities)
        self.patterns = list(patterns)
        self.strictness = strictness
        
    def __repr__(self) -> str:
        pass

    def __len__(self) -> int:
        return len(self.patterns)
   
    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Entity:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.entities[self.n]

    def __getitem__(self, identifier: int or object) -> object:
        if type(identifier) == int:
            return self.patterns[identifier]
        elif type(identifier) == Pattern:
            return self.mostSimilarPattern(identifier)

    def __contains__(self, pattern: Pattern) -> bool:
        output = self % pattern >= self.strictness
        return output

    def __mod__(self, pattern: Pattern or object) -> int:
        if type(pattern) == Pattern:
            return self.similarity(pattern)
        return sum([e1 % e2 for e1, e2 in zip(self, pattern)])

    def __iadd__(self, pattern: pattern or list[Pattern]) -> None:
        if type(pattern) == list:
            for patt in pattern:
                self += patt
        else:
            self.patterns.append(pattern)

    def contains(self, pattern: Pattern) -> bool:
        return pattern in self.patterns or pattern in self.entities

    def similarity(self, entity: Entity) -> int:
        return sum([ent % entity for ent in self])

    def patternsBySimilarity(self, pattern: Entity) -> dict[int or float: Entity]:
        output = {}
        for patt in self:
            output[patt % pattern] = patt
        return output

    def similaritiesByPattern(self, pattern: Pattern) -> dict[Entity: int or float]:
        output = {}
        for patt in self:
            output[patt] = patt % pattern
        return output

    def mostSimilarPattern(self, entity: Entity) -> tuple[int or float, Entity]:
        pbs = self.patternsBySimilarity(entity)
        maximum = max(bs.keys())
        return maximum, pbs[maximum]

    def highestSimilarity(self, entity: Entity) -> Entity:
        ebs = self.entitiesBySimilarity(entity)
        return max(ebs.keys())

class PatternRecognitionEngine:
    def __init__(self, *ctxs: list[Context], strictness: float=0.8, selfImprove: bool=True) -> None:
        self.contexts = ctxs
        self.selfImprove = selfImprove
        self.strictness = strictness

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Entity:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.contexts[self.n]

    def __mod__(self, pattern: Pattern or Context) -> float or int:
        return sum([pattern % ctx for ctx in self])

    def __contains__(self, pattern: Pattern or Context) -> bool:
        return self % pattern >= self.strictness

    def __rshift__(self, item: Pattern or Context) -> Pattern or Context:
        cbs = self.contextsBySimilarity(item)
        best = cbs[max(cbs.keys())]
        if self.selfImprove and type(item) == Context and item in self:
            self.contexts.apppend()

    def contextsBySimilarity(self, pattern: Pattern or Context) -> dict[int or float: Context]:
        return {ctx % pattern: ctx for ctx in self}
