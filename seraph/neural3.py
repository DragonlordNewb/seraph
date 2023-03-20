from typing import Union
import math

from seraph import utils

ACTIVATION = "activation"
DERIVATIVE = "derivative"
INPUT = 0
OUTPUT = -1

class ActivationFunction:
	def __init__(self, activation: Union[utils.function, None]=None, derivative: Union[utils.function, None]=None) -> None:
		if activation != None:
			self.activation = activation
		if derivative != None:
			self.derivative = derivative
		assert hasattr(self, "activation"), "Must subclass a \"activation(self, x)\" method onto ActivationFunction class."
		assert hasattr(self, "derivative"), "Must subclass a \"derivative(self, x)\" method onto ActivationFunction class."
		assert type(self(ACTIVATION, [1, 0])) in [int, float], "Activation function must return an int or float."
		assert type(self(DERIVATIVE, [1, 0])) in [int, float], "Derivative function must return an int or float."
		
	def __repr__(self) -> str:
		return "<seraph.ActivationFunction " + self.__name__ + ">"
	
	def __call__(self, mode: ACTIVATION or DERIVATIVE, x: Union[int, float]) -> Union[int, float]:
		if mode == ACTIVATION:
			return self.activation(x)
		elif mode == DERIVATIVE:
			return self.derivative(x)
		raise SyntaxError("\"mode\" argument of calling an ActivationFunction must be ACTIVATION or DERIVATIVE.")
		
class Sigmoid(ActivationFunction):
	def activation(self, x):
		return 1 / (1 + math.exp(-x))

	def derivative(self, x):
		return self.activation(x) * (1 - self.activation(x))

class Neuron:
	parentLayer = None

	def __init__(self, activation: ActivationFunction=Sigmoid()) -> None:
		self.inputs = []
		self.output = None
		self.inputAxons = []
		self.outputAxons = []
		
		self.activation = activation
	
	def __repr__(self) -> str:
		inl, outl = len(self)
		return "<seraph.Neuron: " + str(inl) + " inputs to " + str(outl) + " outputs, activation=" + repr(self.activation) + ">"

	def __len__(self) -> tuple[int, int]:
		return (len(self.inputAxons), len(self.outputAxons))
		
	def __lshift__(self, values: list[Union[int or float]]) -> list[Union[int, float]]:
		if len(values) != 1:
			for value in values:
				self << value
		else:
			self.inputs.append(values[0])

	def __rshift__(self, obj: object) -> None:
		obj << self.output or ~self

	def __invert__(self) -> Union[int, float]:
		self.output = self.activation(ACTIVATION, self.inputs)
		return self.output

	def wipe(self) -> None:
		self.inputs = []
		self.output = None

	def run(self) -> Union[int, float]:
		output = ~self
		for axon in self.outputAxons:
			self >> axon
		return output

class Axon:
	frontLayer = None
	backLayer = None

	def __init__(self, weight, front: Neuron, back: Neuron) -> None:
		self.weight = weight
		self.front = front
		self.back = back
		
	def __repr__(self) -> str:
		return "<Axon from " + repr(self.front) + " to " + repr(self.back) + ">"
	
	def __lshift__(self, value: Union[int, float]) -> Union[int, float]:
		throughput = value * self.weight
		self.back << throughput
		return throughput

class Layer:
	def __init__(self, *neurons: list[Neuron]) -> None:
		self.neurons = neurons

		self.inputs = []
		self.outputs = []

		for neuron in self:
			neuron.parentLayer = self
			for axon in neuron.inputAxons:
				axon.backLayer = self
			for axon in neuron.outputAxons:
				axon.frontLayer = self

	def __repr__(self) -> str:
		return "<seraph.Layer containing " + ", ".join(repr(neuron) for neuron in self) + ">"

	def __len__(self) -> int:
		return len(self.neurons)

	def __iter__(self) -> object:
		self.n = -1
		return self

	def __next__(self) -> Neuron:
		self.n += 1
		if self.n >= len(self):
			raise StopIteration
		return self[self.n]

	def __getitem__(self, index: int) -> Neuron:
		return self.neurons[index]

	def __lshift__(self, inputs: list[Union[int, float]]) -> None:
		for neuron in self:
			neuron << inputs

	def __rshift__(self, obj: object) -> None:
		obj << self.outputs

	def __invert__(self) -> list[Union[int, float]]:
		self.output = [~neuron for neuron in self]
		return self.output

	def run(self) -> list[Union[int, float]]:
		self.output = [neuron.run() for neuron in self]
		return self.output

	def wipe(self) -> None:
		for neuron in self:
			neuron.wipe()

class FeedforwardNeuralNetwork:
	def __init__(self, *layers: list[Layer]) -> None:
		self.layers = layers

	def __repr__(self) -> str:
		return "<seraph.FeedforwardNeuralNetwork with layers\n" + "\n  ".join([repr(layer) for layer in self]) + "\n(length " + str(len(self)) + ")>"

	def __len__(self) -> int:
		return len(self.layers)

	def __iter__(self) -> object:
		self.n = -1
		return self

	def __next__(self) -> Layer:
		self.n += 1
		if self.n >= len(self):
			raise StopIteration
		return self[self.n]

	def __getitem__(self, index: int) -> Layer:
		return self.layers[index]

	def __lshift__(self, inputs: list[Union[int, float]]) -> None:
		self[INPUT] << inputs

	def wipe(self) -> None:
		for layer in self:
			layer.wipe()

	def predict(self, *inputs) -> list[Union[int, float]]:
		self.wipe()

		self << inputs

		for layer in self:
			layer.run()

		return self[OUTPUT].outputs