import math
import numpy 

from typing import Union
from seraph import utils

activationFunctions = {
	"sigmoid": (lambda x: 1 / (1 + math.exp(-x)), lambda x: (1 / (1 + math.exp(-x))) * (1 - (1 / (1 + math.exp(-x)))))
}

def mse(expected: list[Union[int, float]], predicted: list[Union[int, float]]) -> Union[int, float]:
	print("Calculating MSE on " + str(expected) + " and " + str(predicted))
	if type(expected) != list:
		expected = [expected for _ in range(len(predicted))]
	n = len(expected)
	
	error = 0.0
	for i in range(n):
		error += (predicted[i] - expected[i]) ** 2
	mse = error / n
	return mse

class Neuron:
	parentLayer = None

	def __init__(self, inputs: int, activationFunction: str="sigmoid", mu: int or float=0, sigma: int or float=0.1) -> None:
		self.weights = list(numpy.random.normal(mu, sigma, inputs).astype(int))
		self.bias = 0
		self.activate, self.derivative = activationFunctions[activationFunction]
		self.inputs = [0] * inputs
		self.output = 0
		
	def __len__(self) -> int:
		return len(self.weights)

	def feedforward(self, inputs: list[Union[int, float]]) -> Union[int, float]:
		print("Neuron feedforward on inputs: " + str(inputs))
		if type(inputs) != list:
			inputs = [inputs]
		self.inputs = inputs
		weightedSum = sum(x * w for x, w in zip(inputs, self.weights))
		self.output = self.activate(weightedSum + self.bias)
		return self.output
	
	def error(self, expected: Union[int, float]) -> Union[int, float]:
		print("Error calculation: output=" + str(self.output) + ", expected=" + str(expected))
		if type(expected) == list:
			expected = expected[0]

		delta = self.output - expected
		try:
			out = math.sqrt(delta)
		except ValueError:
			out = math.sqrt(-delta)

		print("Error: " + str(out))
		return out
		# old:
		# return self.derivative(self.output * abs(expected - self.output))
		
class Layer:
	isOutput = False

	def __init__(self, neurons: list[Neuron]) -> None:
		self.neurons = neurons

		for neuron in self:
			neuron.parentLayer = self

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
	
	def error(self, expected: list[Union[int, float]]) -> Union[int, float]:
		return sum([neuron.error(expected) for neuron in self])
	
	def feedforward(self, inputs: list[Union[int, float]]) -> list[Union[int, float]]:
		return [neuron.feedforward(inputs) for neuron in self]
	
	def backpropagate(self, expected: list[Union[int, float]], learningRate: Union[int, float]) -> Union[int, float]:
		print("Executing layer backpropagation ...")
		with utils.Indent():
			errors = [neuron.error(expected) for neuron in self]
			print("Errors: " + str(errors))

			for neuron, error in zip(self, errors):
				grad = neuron.derivative(neuron.output) * error

				neuron.bias += grad * learningRate

				for index in range(min(len(neuron.weights), len(neuron.inputs))):
					neuron.weights[index] += grad * neuron.inputs[index] * learningRate

		return sum(errors)

class OutputLayer(Layer):
	isOutput = True

class InputLayer(Layer):
	def backpropagate(self, *args, **kwargs) -> None:
		return 0

class NeuralNetwork:
	def __init__(self, layers: list[Layer]) -> None:
		self.layers = layers

		for index, layer in enumerate(self.layers[1:]):
			layer.lastLayer = self[index - 1]

		self.outputs = []

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
	
	def feedforward(self, inputs):
		self.outputs =  []
		print("Executing feedforward loop ...")
		with utils.Indent():
			for layer in self:
				lastInputs = inputs
				
				inputs = layer.feedforward(inputs)
				print("Previous inputs: " + str(lastInputs) + " - " + str(inputs))
				self.outputs.append(inputs)
		print("Feedforward finished.")
		return inputs
	
	def backpropagate(self, expected: list[Union[int, float]], learningRate: Union[int, float]) -> None:
		print("Executing backpropagation loop ...")
		with utils.Indent():
			if type(expected) != list:
				expected = [expected]
			error = [a - b for a, b in zip(expected, self.outputs[-1])]
			print("Calculated errors: " + str(error))
			for i in range(len(self.layers) - 1, -1, -1):
				print("Layer number: " + str(i))
				error = self.layers[i].backpropagate(error, learningRate)

	def train(self, inputs: list[list[float]], expected_outputs: list[list[float]], epochs: int, learning_rate: float) -> None:
		for epoch in range(epochs):
			total_loss = 0.0
			for x, y_true in zip(inputs, expected_outputs):
				# forward propagation
				y_pred = self.feedforward(x)
				
				# calculate loss
				loss = mse(y_true, y_pred)
				total_loss += loss
				
				# backward propagation
				self.backpropagate(y_true, learning_rate)
			
			# print average loss for each epoch
			avg_loss = total_loss / len(inputs)
			print(f"Epoch {epoch}: loss={avg_loss:.4f}")

def assembleNeuralNetwork(layerSizes, activationFunction="sigmoid", mu=0, sigma=0.1):
	layers = []
	for i in range(len(layerSizes)):
		if i == 0:
			# Input layer
			layer = Layer([Neuron(layerSizes[0])])
		elif i == len(layerSizes) - 1:
			# Output layer
			layer = OutputLayer([Neuron(layerSizes[-2]) for _ in range(layerSizes[-1])])
		else:
			# Hidden layer
			layer = Layer([Neuron(layerSizes[i-1], activationFunction, mu, sigma) for _ in range(layerSizes[i])])
		layers.append(layer)
	return NeuralNetwork(layers)

class Schematic:
	def __init__(self, layerSizes, activationFunction="sigmoid", mu=0, sigma=0.1):
		self.layerSizes = layerSizes
		self.activationFunction = activationFunction
		self.mu = mu
		self.sigma = sigma

	def assemble(self):
		assembleNeuralNetwork(self.layerSizes, self.activationFunction, self.mu, self.sigma)
