import random
import math

LEARNING_RATE = 0.01

sigmoid, derivative = lambda x: 1 / (1 + math.exp(-x)), lambda x: (1 / (1 + math.exp(-x))) * (1 - (1 / (1 + math.exp(-x))))
def sgn(x):
	if x > 0:
		return 1
	if x < 0:
		return -1
	return 0

def generateNormalDistribution(mu, sigma, size):
	points = []
	for i in range(size // 2):
		u1 = random.random()
		u2 = random.random()
		z1 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
		z2 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2 * math.pi * u2)
		x1 = mu + sigma * z1
		x2 = mu + sigma * z2
		points.append(x1)
		points.append(x2)
	if size % 2 != 0:
		u1 = random.random()
		u2 = random.random()
		z1 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
		x = mu + sigma * z1
		points.append(x)
	return points

# Lux's Neural Network Designs! 

class Neuron:
	def __init__(self, inputCount: int) -> None:
		self.weights = generateNormalDistribution(1, 1, inputCount)
		self.bias = 0
		self.inputs = []

	def __len__(self) -> int:
		return len(self.weights)
				
	def feedforward(self, inputs: list[int or float]) -> int or float:
		self.inputs = inputs
		assert len(inputs) == len(self), "Must take the correct number of inputs (in this case " + str(len(self)) + ")"

		weightedSum =  sum([i * w for i, w in zip(inputs, self.weights)])
		return sigmoid(weightedSum + self.bias)
	
	def calculateError(self, inputs: list[int or float], expected: int or float) -> int or float:
		delta = self.feedforward(inputs) - expected
		return sgn(delta) * math.sqrt(abs(delta))
	
	def backpropagate(self, errors: list[int or float]) -> None:
		for index in range(len(self)):
			self.weights[index] += LEARNING_RATE * errors[index] * self.inputs[index]
		
		self.bias += LEARNING_RATE * sum(errors)

class Layer:
	def __init__(self, *neurons: list[Neuron]) -> None:
		self.neurons = neurons

	def __len__(self) -> int:
		return len(self.neurons)
	
	def __iter__(self) -> object:
		self.n = -1
		return self
	
	def __next__(self) -> Neuron:
		self.n += 1 
		if self.n >= len(self):
			raise StopIteration
		return self.neurons[self.n]

	def feedforward(self, inputs: list[int or float]) -> list[int or float]:
		return [neuron.feedforward(inputs) for neuron in self]

	def calculateErrors(self, inputs: list[int or float], expected: list[int or float]) -> list[int or float]:
		return [neuron.calculateError(inputs, expected) for neuron in self]
	
	def backpropagate(self, inputs: list[int or float], expected: list[int or float]) -> None:
		errors = self.calculateErrors(inputs, expected)
		for neuron in self:
			neuron.backpropagate(errors)

class NeuralNetwork:
	def __init__(self, *layers: list[Layer]) -> None:
		self.layers = layers
		self.inputs = None
		self.output = None

	def __len__(self) -> int:
		return len(self.layers)
	
	def __iter__(self) -> object:
		self.n = -1
		return self
	
	def __next__(self) -> Neuron:
		self.n += 1 
		if self.n >= len(self):
			raise StopIteration
		return self.layers[self.n]
	
	def feedforward(self, inputs: list[int or float]) -> list[int or float]:
		self.inputs = inputs
		for layer in self:
			inputs = layer.feedforward(inputs)
		self.output = inputs
		return inputs

	def feedbackward(self, expected: list[int or float]) -> None:
		for layer in [layer for layer in reversed(self)]:
			layer.backpropagate(self.inputs, expected)

	def adapt(self, inputs: list[list[int or float]], expected: list[list[int or float]]):
		for x, y in zip(inputs, expected):
			self.feedforward(x)
			self.feedbackward(y)

	def train(self, inputs: list[list[int or float]], expected: list[list[int or float]], epochs: int=1000):
		for epoch in range(epochs):
			self.adapt(inputs, expected)

	def predict(self, inputs: list[int or float]) -> list[int or float]:
		return self.feedforward(inputs)
	
	def duplicate(self) -> object:
		return NeuralNetwork(self.layers)
	
class NeuralNetworkSchematic:
	def __init__(self, inputCount: int, sizes: list[int]) -> None:
		self.sizes = sizes
		self.inputCount = inputCount

	def assemble(self) -> NeuralNetwork:
		layers = [Layer(*[Neuron(self.inputCount) for _ in range(self.sizes[0])])]

		for index, size in enumerate(self.sizes[1:]):
			layers.append(Layer(*[Neuron(self.sizes[index - 1]) for _ in range(size)]))

		return NeuralNetwork(*layers)
	
	def extend(self, size: int or None=None) -> None:
		if size:
			self.sizes.append(size)
		else:
			self.sizes.append(self.sizes[-1])
	
class BiconicNeuralNetworkSchematic(NeuralNetworkSchematic):
	def __init__(self, inputCount: int, initialHeight: int, hiddenHeight: int, width: int) -> None:
		NeuralNetworkSchematic.__init__(self, inputCount, [initialHeight] + [hiddenHeight for _ in range(width)] + [initialHeight])