import random

from seraph import entity as _entity
from seraph import utils

class OverextensionError(RuntimeError):
	pass

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

	def __add__(self, other: object) -> object:
		return Cluster(self.entities + other.entities)

	def __mod__(self, other: object) -> int or float:
		return sum([e1 % e2 for e1, e2 in zip(self, other)])
		
	def addEntity(self, entity: _entity.Entity) -> None:
		self.entities.append(entity)
		
	def pack(self, threshold: int, recursion: int=0) -> list[object]:
		if recursion:
			packing = self.pack(threshold, 0)
			result = []
			for cluster in packing:
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
			if max(ebs.keys()) >= threshold:
				output.append(Cluster(*currentList))
				currentList = []
			currentIndex = ebs[max(ebs.keys())]

		return output

	def crack(self, n: int, recursion: int=0):
		initial = self[0]
		thresholds = [self[0] % entity for entity in [ent for ent in self][1:]]
		thresholds.sort()
		threshold = thresholds[n]
		return self.pack(threshold, recursion)

class ClusterTree:
	def __init__(self, *entities: list[_entity.Entity]) -> None:
		self.entities = entities
		self.clusters = [Cluster(*[entity for entity in self.entities])]
		self.layers = [self.clusters]

	def __repr__(self) -> str:
		return "<seraph.cluster.ClusterTree of length " + str(len(self)) + ">"

	def __len__(self) -> int:
		return len(self.entities)

	def __getitem__(self, index: int) -> list[Cluster]:
		return self.layers[index]

	def _extendOnce(self) -> list[Cluster]:
		if len(self.layers[-1]) > 2:
			raise OverextensionError
		clusters = self.layers[-1]

		newClusters = []
		while len(clusters) > 1:
			current = clusters.pop(random.randint(0, len(clusters)))
			clustersBySimilarity = {current % c: i for i, c in enumerate(clusters)}
			highestSimilarity = max(clustersBySimilarity.keys())
			newClusters.append(current + clusters.pop(clustersBySimilariy[highestSimilarity]))

		newClusters.append(Cluster(clusters[0]))
		
		self.layers.append(newClusters)
		return newClusters

	def extend(self, n: int=1) -> list[Cluster]:
		output = None
		for _ in range(n):
			try:
				output = self._extendOnce()
			except OverextensionError as e:
				if output:
					return output
				raise e
		return output