from seraph import entity as _entity

class Pattern:
    def __init__(self, *entities: list[_entity.Entity]):
        self.entities = entities

class PatternRecognitionEngine:
    def __init__(self, *patterns:)