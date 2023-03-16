from seraph import entity
from seraph.common import *

class Action(entity.Entity):
	sequence = ACTION
	def __init__(self, 
				*properties: list[entity.Property or entity.Entity], 
				strictness: int=0.8,
				parent: object or None=None) -> None:
		entity.Entity.__init__(self, *properties, strictness=strictness)
		self.parent = parent

	def setParent(self, parent: object) -> None:
		self.parent = parent

class Reaction(Action):
	sequence = REACTION

class ActionReactionPair:
	def __init__(self, actions: Action or list[Action], reaction: Reaction or list[Reaction]) -> None:
		self.actions = actions
		self._actionClassifier = entity.Classifier(*self.actions)
		self.reaction = reaction
		self._reactionClassifier = entity.Classifier(*self.reactions)
		
	def __repr__(self) -> str:
		return "<ActionReactionPair " + str(self.actions) + " -> " + str(self.reactions) + ">"

	def __len__(self) -> tuple[int, int]:
		return (len(self.actions), len(self.reactions))
		
	def __iter__(self) -> object:
		self.n = -1
		self.itermode = ACTION
		return self
	
	def __next__(self) -> Action or Reaction or SEQBREAK:
		self.n += 1
		if self.itermode == ACTION:
			if self.n >= len(self.actions):
				self.itermode = REACTION
				self.n = -1
				return SEQBREAK
			return self.actions[self.n]
		else:
			if self.n >= len(self.reactions):
				raise StopIteration
			return self.reactions[self.n]
