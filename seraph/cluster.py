from seraph import entity as _entity
from seraph import utils

class Cluster:
	def __init__(self, *entities: list[_entity.Entity]):
		self.entities = entities
		
	def __len__(self) -> int:
		return len(self.entities)
	
	def __getitem__(self, index: int) -> _entity.Entity:
		return self.entities[index]
	
	def __iter__(self) -> object:
		self.n = -1
		return self
	
	def __next__(self) -> _entity.Entity:
		self.n += 1
		if self.n >= len(self):
			raise StopIteration
		return self[self.n]
		
	def addEntity(self, entity: _entity.Entity) -> None:
		self.entities.append(entity)
		
	def pack(self, threshold: int, recursion: int=0) -> list[object]:
		if recursion:
			packing = self.pack(threshold, 0)
			result = []
			for cluster in packing
				result.append(cluster.pack(threshold, recursion - 1))
			return result
		
		database = [entity for entity in self]
		output = []
		currentList = []
		currentIndex = 0
		while len(database) > 0:
			ent = database.pop(currentIndex)
			currentList.append(ent)
			ebs = {ent % other: index for index, other in enumerate(database)}
			if min(ebs.keys()) >= threshold:
				output.append(Cluster(*currentList))
				currentList = []
			currentIndex = ebs[min(ebs.keys())]

		return output