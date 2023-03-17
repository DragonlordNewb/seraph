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
	def __init__(self, actions: Action or list[Action], reactions: Reaction or list[Reaction]) -> None:
		if type(actions) == Action:
			actions = [action]
		if type(reactions) == Reaction:
			reactions = [reactions]
			
		for action in actions:
			action.setParent(self)
		for reaction in reactions:
			reaction.setParent(self)

		self.actions = actions
		self._actionClassifier = entity.Classifier(*self.actions)
		self.reactions = reactions
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
		
	def __mod__(self, other: object) -> int:
		return min(self.causedBy(*other.actions), self.causes(*other.reactions))
	
	def causedBy(self, *actions: list[Action]) -> int:
		return sum([a1 % a2 for a1, a2 in zip(self.actions, actions)])
	
	def causes(self, *reactions: list[Reaction]) -> int:
		return sum([r1 % r2 for r1, r2 in zip(self.reactions, reactions)])