from typing import Union
import math

from seraph import utils
from seraph.common import ActivationFunction, LossFunction, Sigmoid, MeanSquareError

ACTIVATION = "activation"
DERIVATIVE = "derivative"
LOSS = "loss"
GRADIENT = "gradient"
INPUT = 0
OUTPUT = -1

class Sigmoid(ActivationFunction):
	def activation(self, x):
		return 1 / (1 + math.exp(-x))

	def derivative(self, x):
		return self.activation(x) * (1 - self.activation(x))

class MeanSquareError(LossFunction):
	def loss(self, reality, prediction):
		assert len(reality) == len(prediction), "Can't compare reality and prediction arguments of different length."
		return sum([(p - r) ** 2 for r, p in zip(reality, prediction)]) / len(reality)

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

	def weightMatrix(self) -> list[Union[int, float]]:
		return [sum(neuron.weights) / len(neuron.weights) for neuron in self]

	def run(self) -> list[Union[int, float]]:
		self.output = [neuron.run() for neuron in self]
		return self.output

	def wipe(self) -> None:
		for neuron in self:
			neuron.wipe()

class FeedforwardNeuralNetwork:
	def __init__(self, *layers: list[Layer], loss: LossFunction=MeanSquareError()) -> None:
		self.layers = layers
		self.loss = loss

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

	def reversed(self) -> list[Layer]:
		return [layer for layer in self][::-1]

	def wipe(self) -> None:
		for layer in self:
			layer.wipe()

	def predict(self, *inputs) -> list[Union[int, float]]:
		self.wipe()

		self << inputs

		for layer in self:
			layer.run()

		return self[OUTPUT].outputs

	def backpropagate(self, *reality: list[Union[int, float]], learningRate: int=0.01) -> list[Union[int, float]]:
		outputLayerGradient = self.loss(GRADIENT, list(reality), self[OUTPUT].outputs)
		outputInverse = [neuron.activation(DERIVATIVE, neuron.output) for neuron in self[OUTPUT]]
		outputError = [x * y for x, y in zip(outputLayerGradient, outputInverse)]

		errors = [outputError]

		for layer in enumerate(list(self.reversed())[1:]):

			# δ^l = ((W^{l+1})^T δ^{l+1}) ⊙ f'(z^l)
			errors.append([x * y for x, y in zip(errors[-1], layer.weightMatrix())])

		errors = errors[::-1]

		for layerIndex, layer in enumerate(self):
			for neuronIndex, neuron in enumerate(layer):
				neuron.bias += learningRate * errors[layerIndex][neuronIndex]
				for index, weight in enumerate(neuron.weights):
					neuron.weights[index] += learningRate * neuron.output * errors[layerIndex][neuronIndex]

		return errors

	def train(self, samples: list[tuple[list[Union[int, float]], list[Union[int, float]]]], epochs: int=1000, learningRate: int=0.01) -> None:
		for epoch in range(epochs):
			for inputs, outputs in samples:
				self.predict(inputs)
				self.backpropagate(*outputs, learningRate=learningRate)
