from seraph import entity as _entity

class Pattern:
    def __init__(self, *entities: list[_entity.Entity]) -> None:
        self.entities = entities

class Context:
    def __init__(self, *patterns: list[Pattern], strictness: int=.8, selfImprove: bool=False) -> None:
        self.patterns = list(entities)
        self.strictness = strictness
        self.selfImprove = selfImprove

    def __repr__(self) -> str:
        return "<seraph.precog.Context of length " + str(len(self)) + ">"
    
    def __len__(self) -> int:
        return len(self.class Classifier(utils.Summarizable, utils.Makeable):
    def __init__(self, *entities: list[Entity], strictness: int=.8, selfImprove: bool=False) -> None:
        self.entities = list(entities)
        self.strictness = strictness
        self.selfImprove = selfImprove

    def __repr__(self) -> str:
        return "<seraph.Classifier of length " + str(len(self)) + ">"
    
    def __len__(self) -> int:
        return len(self.entities)

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
            return self.entities[identifier]
        elif type(identifier) == Entity:
            return self.mostSimilarEntity(identifier)

    def __contains__(self, entity: Entity) -> bool:
        output = self % entity >= self.strictness
        if output and self.selfImprove:
            self += entity
        return output

    def __mod__(self, entity: Entity) -> int:
        return self.similarity(entity)

    def __iadd__(self, entity: Entity or list[Entity]) -> None:
        if type(entity) == list:
            for ent in entity:
                self += ent
        else:
            self.entities.append(entity)

    def contains(self, entity: Entity) -> bool:
        return entity in self.entities

    def similarity(self, entity: Entity) -> int:
        return sum([ent % entity for ent in self])

    def entitiesBySimilarity(self, entity: Entity) -> dict[int or float: Entity]:
        output = {}
        for ent in self:
            output[ent % entity] = ent
        return output

    def similaritiesByEntity(self, entity: Entity) -> dict[Entity: int or float]:
        output = {}
        for ent in self:
            output[ent] = ent % entity
        return output

    def mostSimilarEntity(self, entity: Entity) -> tuple[int or float, Entity]:
        ebs = self.entitiesBySimilarity(entity)
        maximum = max(ebs.keys())
        return maximum, ebs[maximum]

    def highestSimilarity(self, entity: Entity) -> Entity:
        ebs = self.entitiesBySimilarity(entity)
        return max(ebs.keys()))

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
            return self.entities[identifier]
        elif type(identifier) == Entity:
            return self.mostSimilarEntity(identifier)

    def __contains__(self, entity: Entity) -> bool:
        output = self % entity >= self.strictness
        if output and self.selfImprove:
            self += entity
        return output

    def __mod__(self, entity: Entity) -> int:
        return self.similarity(entity)

    def __iadd__(self, entity: Entity or list[Entity]) -> None:
        if type(entity) == list:
            for ent in entity:
                self += ent
        else:
            self.entities.append(entity)

    def contains(self, entity: Entity) -> bool:
        return entity in self.entities

    def similarity(self, entity: Entity) -> int:
        return sum([ent % entity for ent in self])

    def entitiesBySimilarity(self, entity: Entity) -> dict[int or float: Entity]:
        output = {}
        for ent in self:
            output[ent % entity] = ent
        return output

    def similaritiesByEntity(self, entity: Entity) -> dict[Entity: int or float]:
        output = {}
        for ent in self:
            output[ent] = ent % entity
        return output

    def mostSimilarEntity(self, entity: Entity) -> tuple[int or float, Entity]:
        ebs = self.entitiesBySimilarity(entity)
        maximum = max(ebs.keys())
        return maximum, ebs[maximum]

    def highestSimilarity(self, entity: Entity) -> Entity:
        ebs = self.entitiesBySimilarity(entity)
        return max(ebs.keys())

class PatternRecognitionEngine:
    def __init__(self, *patterns:)