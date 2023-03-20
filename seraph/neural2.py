import math
import random
import tqdm

def sigmoid(x):
	if type(x) == list:
		return sigmoid(sum(x) / len(x))
	return 1 / (1 + math.exp(-x))

def sigmoidDerivative(x):
	if type(x) == list:
		return sigmoidDerivative(sum(x) / len(x))
	return sigmoid(x) * (1 - sigmoid(x))

LEARNING_RATE = 0.001

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

def meanSquareError(expected: list[int or float], prediction: list[int or float]) -> int or float:
	if type(expected) != list:
		expected = [expected]

	if type(prediction) != list:
		prediction = [prediction]

	n = len(expected)
	assert n == len(prediction), "Can't compute MSE for lists of different length."
	
	return (1 / n) * sum([(expected[x] - prediction[x]) ** 2 for x in range(n)])

def meanSquareErrorDerivative(expected: list[int or float], prediction: list[int or float]):
	if type(expected) != list:
		expected = [expected]

	if type(prediction) != list:
		prediction = [prediction]

	n = len(expected)
	assert n == len(prediction)

	return (2 / n) * sum([prediction[x] - expected[x] for x in range(n)])

class Neuron:
	parentLayer = None

	def __init__(self, inputCount: int) -> None:
		self.weights = generateNormalDistribution(1, 1, inputCount)
		self.bias = 0

		self.inputs = None
		self.output = None

	def __len__(self) -> int:
		return len(self.weights)
		
	def __lshift__(self, inputs: list[int or float]) -> int or float:
		self.inputs = inputs
		self.output = sigmoid(inputs)
		return self.output

	def sigmoid(self, inputs):
		return sigmoid(sum([i * w for i, w in zip(inputs, self.weights)]))

	def sigmoidDerivative(self, inputs) -> int or float:
		return sigmoidDerivative(sum([i * w for i, w in zip(inputs, self.weights)]))

	def delta(self):
		s = 1
		if self.parentLayer.lastLayer != None:
			s = sum([self.weights[x] * self.parentLayer.lastLayer[x].delta() for x in range(len(self))])
		return sigmoidDerivative([self.inputs[x] * self.weights[x] for x in range(len(self))]) * s

class Layer:
	parentNetwork = None
	nextLayer = None
	lastLayer = None

	def __init__(self, *neurons: list[Neuron]) -> None:
		self.neurons = neurons

		for neuron in self:
			neuron.parentLayer = self

		self.inputs = None
		self.output = None

	def __len__(self) -> int: 
		return len(self.neurons)

	def __getitem__(self, index: int) -> Neuron:
		return self.neurons[index]

	def __iter__(self) -> object:
		self.n = -1
		return self

	def __next__(self) -> Neuron:
		self.n += 1
		if self.n >= len(self):
			raise StopIteration
		return self[self.n]

	def __lshift__(self, inputs: list[int or float]) -> list[int or float]: # feedforward function
		self.inputs = inputs
		self.output = []
		for neuron in self:
			self.output.append(neuron << inputs)
		return self.output

	def __rshift__(self, error: int or float) -> None: # backpropagation function
		biasGradient = error
		weightGradients = [0] * len(self)
		if self.lastLayer != None:
			weightGradient = [o * error for o in self.lastLayer.output]
		
		for neuron in self:
			neuron.bias -= LEARNING_RATE * biasGradient

		for neuron in self:
			for index in range(len(neuron)):
				neuron.weights[index] -= LEARNING_RATE * weightGradients[index]

class FeedforwardNeuralNetwork:
	def __init__(self, *layers: list[Layer]) -> None:
		self.layers = layers
		
		for index, layer in enumerate(self.layers):
			layer.parentNetwork = self

			if index not in [0, len(self) - 1]:
				layer.lastLayer = self.layers[index - 1]
				layer.nextLayer = self.layers[index + 1]

		self.inputs = None
		self.output = None

	def __len__(self) -> int: 
		return len(self.layers)

	def __getitem__(self, index: int) -> Neuron:
		return self.layers[index]

	def __iter__(self) -> object:
		self.n = -1
		return self

	def __next__(self) -> Neuron:
		self.n += 1
		if self.n >= len(self):
			raise StopIteration
		return self[self.n]

	def __lshift__(self, inputs: list[int or float]) -> list[int or float]: # feedforward function
		self.inputs = inputs
		for layer in self:
			self.inputs = layer << self.inputs
		self.output = self.inputs
		return self.output
	
	def __rshift__(self, expected: list[int or float]) -> None:
		err = self.error(expected)

		reversedLayers = reversed([layer for layer in self])
		for layer in reversedLayers:
			layer >> err

	def error(self, expected: list[int or float]) -> list[int or float]:
		return meanSquareError(expected, self.output)

	def train(self, inputs: list[int or float], expected: list[int or float], epochs: int=1000):
		for _ in tqdm.tqdm(range(epochs)):
			for inputs, expected in zip(inputs, expected):
				self << inputs
				self >> expected

	def predict(self, inputs: list[int or float]) -> list[int or float]:
		return self << inputs

class NeuralNetworkSchematic:
	def __init__(self, sizes: list[int]):
		self.sizes = sizes

	def assemble(self) -> FeedforwardNeuralNetwork:
		layers = []
		count = 1

		for size in self.sizes:
			layers.append(Layer(*[Neuron(count) for _ in range(size)]))
			count = size

		return FeedforwardNeuralNetwork(*layers)