from seraph import entity as _entity

class Pattern:
    def __init__(self, *entities: list[_entity.Entity]) -> None:
        self.entities = entities

class Context:
    def __init__(self, *patterns: list[Pattern], strictness: int=.8) -> None:
        self.patterns = list(entities)
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
        return self.patterns[self.n]

    def __getitem__(self, identifier: int or object) -> object:
        if type(identifier) == int:
            return self.patterns[identifier]
        elif type(identifier) == Pattern:
            return self.mostSimilarPattern(identifier)

    def __contains__(self, pattern: Pattern) -> bool:
        output = self % pattern >= self.strictness
        return output

    def __mod__(self, pattern: Pattern) -> int:
        return self.similarity(pattern)

    def __iadd__(self, pattern: pattern or list[Pattern]) -> None:
        if type(pattern) == list:
            for patt in pattern:
                self += patt
        else:
            self.patterns.append(pattern)

    def contains(self, pattern: Pattern) -> bool:
        return pattern in self.patterns

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
    def __init__(self, *patterns:)
