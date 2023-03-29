from seraph import entity as _entity

class Pattern:
	def __init__(self, *entities: list[_entity.Entity], strictness: int=0.8) -> None:
		self.entities = entities
		self.strictness = strictness

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
		return self.pattern[self.n]

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

				pattern = Pattern(*block, strictness=strictness)
				confidence = equality / (len(blocks) - 1)
				sufficient = confidence >= strictness

				patterns.append((
					pattern,
					confidence,
					sufficient
				))

		return [(pattern, confidence) for pattern, confidence, sufficient in patterns if sufficient]

	def __or__(self, pattern: Pattern) -> int, float:
		# PRE | pattern
		# returns how significant pattern is
		# given the existing entities in PRE

		current = self >> 0
		self << pattern
		new = self >> 0
		self.pop()
		currentConfidence = sum([confidence for pattern, confidence in current])
		newConfidence = sum([confidence for patter, confidence in new])
		confidenceDelta = newConfidence - currentConfidence
		totalConfidence = currentConfidence + newConfidence
		newPatternCount = len(new) - len(current)
		adjustedNewPatternCount = newPatternCount * totalConfidence
		return adjustedNewPatternCount + confidenceDelta

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

	def pop(self, index: int=-1) -> _entity.Entity:
		return self.pattern.pop(index)

	def synthesize(self, strictness: int=0.25) -> Pattern:
		return self >> strictness

class PatternAnalyzer:
	def __init__(self, *patterns: list[Pattern], strictness: int=1, selfImprove: bool=True) -> None:
		self.patterns = patterns
		self.strictness = strictness
		self.averageStrictness = lambda: sum([pattern.strictness for pattern in self]) / len(self)

	def __repr__(self) -> str:
		return "<seraph.precog.PatternAnalyzer with " + str(len(self)) + " patterns>"

	def __len__(self) -> int:
		return len(self.patterns)

	def __iter__(self) -> object:
		self.n = -1
		return self

	def __next__(self) -> Pattern:
		self.n += 1
		if self.n >= len(self):
			raise StopIteration
		return self.patterns[self.n]

	def __lshift__(self, obj: object) -> None:
		if type(obj) == Pattern:
			self.patterns.append(obj)
		
		elif hasattr(obj, "__iter__") and hasattr(obj, "__next__"):
			# if the object is an iterable:
			for sub in obj:
				self << sub

		else:
			raise TypeError("Can only use a Pattern or iterable for << with PatternAnalyzer.")

	def __rshift__(self, *obj: Pattern or list[_entity.Entity]) -> Pattern:
		if len(obj) == 1:
			if type(obj[0]) == Pattern:
				return self._predictPattern(obj[0])

			elif type(obj[0]) == list:
				if all([type(x) == Pattern for x in obj[0]]):
					return self._predictEntities(obj[0])

				else:
					raise TypeError("Can only supply lists of Entities.")

			else:
				raise TypeError("Only Patterns or lists of Entities can be used.")

		elif all([type(x) == _entity.Entity for x in obj]):
			return self._predictEntities(list(obj))

		raise TypeError("idek, error message or sm") # fix this??

	def _predictPattern(self, pattern: Pattern) -> list[tuple[Pattern, float or int, bool]]:
		# bool indicates whether the pattern was sufficient

		output = []

		scores = {pattern % patt: patt for patt in self}
		strict = False
		for score in scores.keys():
			patt = scores[score]
			sufficient = score >= self.strictness
			if (not strict) and sufficient:
				strict = True

			output.append((patt, score, sufficient))

		if strict:
			self << pattern

		return output

	def _predictEntities(self, entities: list[_entity.Entity]) -> list[tuple[Pattern, list[tuple[Pattern, float or int, bool]]]]:
		pre = PatternRecognitionEngine()
		for ent in entities:
			pre << ent
		results = pre >> self.averageStrictness()

		output = []
		for pattern, confidence in results:
			if confidence >= self.strictness:
				output.append(self >> pattern)

		return output