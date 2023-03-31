from random import random
from math import exp
from typing import Union

def sigmoid(x):
	return 1 / (1 + exp(-x))

class BadOriginError(Exception):
	pass

class Neuron:
	def __init__(self) -> None:
		self.bias = random()
		self.inputAxons = []
		self.outputAxons = []
		self.inputs = []
		self.output = 0

	def __contains__(self, item: object) -> bool:
		return item in self.inputAxons or item in self.outputAxons
		
	def __lshift__(self, value: Union[int, float]) -> None:
		self.inputs.append(value)

	def __rshift__(self, target: object) -> None:
		if not self.output:
			self.output = self.calculate()
		target << (self.output, self)

	def calculate(self) -> Union[int, float]:
		output = sigmoid(sum(self.inputs))
		self.clear()
		self.output = output
		return self.output
	
	def clear(self):
		self.inputs = []
		self.output = 0
	
class Axon:
	def __init__(self, front: Neuron, back: Neuron) -> None:
		self.front = front
		if self not in self.front.outputAxons:
			self.front.outputAxons.append(self)
		self.back = back
		if self not in self.back.inputAxons:
			self.back.inputAxons.append(self)
		self.weight = random()

	def __lshift__(self, package: tuple[Union[int, float], Neuron]) -> None:
		value, origin = package
		if origin == self.front:
			self.back << value * self.weight
		elif origin == self.back:
			self.front << value * self.weight
			self.weight -= value * self.weight
		else:
			raise BadOriginError("Package must originate from front or back.")
		
class Layer:
	def __init__(self, structure: Union[list[Neuron], int]) -> None:
		if type(structure) == int:
			self.neurons = []
			for _ in range(structure):
				self.neurons.append(Neuron())
		elif type(structure) == list:
			self.neurons = structure

	def __lshift__(self, value: value) -> None:
		for neuron in self:
			neuron << value