# To build a neural network (thank you, ChatGPT):

# Initialize the network:
#
# 	Define the number of input, hidden, and output layers
# 	Randomly initialize the weights and biases for each layer
# 	Define the activation function
# 		For example, you can use the sigmoid function, which takes a weighted sum of inputs and outputs a value between 0 and 1
# 	Define the derivative of the activation function for backpropagation

# Train the network:
#
# Repeat until convergence:
# 	For each training example:
# 		Forward pass: compute the output of the network given the input and current weights
# 		Compute the error between the predicted output and the actual output
# 		Backward pass: compute the gradient of the error with respect to the weights using backpropagation
# 		Update the weights using the learning rate and the gradient

# Test the network:
#
# For each test example:
# 	Forward pass: compute the output of the network given the input and trained weights
# 	Compare the predicted output to the actual output

# And no, I didn't generate this code using ChatGPT. I wrote all this with my own keyboard.
# ChatGPT gave me the outline and I filled it in.

import numpy as np
from tqdm import tqdm

def sigmoid(x, derivative=False):
	if derivative:
		return sigmoid(x) * (1 - sigmoid(x))
	return 1 / (1 + np.exp(-x))

class Neuron:
	def __init__(self, weights, bias):
		self.weights = weights
		self.bias = bias
		self.weighted_sum = 0
	
	def forward(self, inputs):
		self.weighted_sum = np.dot(self.weights, inputs) + self.bias
		activation = sigmoid(self.weighted_sum)
		return activation
	
	def backward(self, error_gradient, inputs, learning_rate):
		activation_gradient = sigmoid(self.weighted_sum, derivative=True)
		self.error_gradient = error_gradient * activation_gradient
		weight_gradients = inputs * self.error_gradient[:, np.newaxis]
		bias_gradient = self.error_gradient.sum()
		self.weights -= learning_rate * weight_gradients
		self.bias -= learning_rate * bias_gradient
		return self.error_gradient

	def sigmoid(self, x: int or float):
		return 1 / (1 + np.exp(-x))

	def sigmoid_derivative(self, x: int or float):
		fx = self.sigmoid(x)
		return fx * (1 - fx)

class Layer:
	def __init__(self, n_inputs, n_neurons):
		self.neurons = [Neuron(n_inputs, 0) for _ in range(n_neurons)]
		self.weights = np.random.randn(n_neurons, n_inputs).astype(np.float64)
		self.bias = np.array([neuron.bias for neuron in self.neurons]).reshape((-1, 1))

	def forward(self, inputs):
		return np.array([neuron.forward(inputs) for neuron in self.neurons])

	def backward(self, error_gradients, inputs, learning_rate):
		# Compute gradients for each neuron in the layer
		neuron_gradients = np.array([neuron.backward(error_gradients[i], inputs, learning_rate) for i, neuron in enumerate(self.neurons)])
		# Compute gradients for weights and biases
		weight_gradients = np.dot(neuron_gradients, inputs.T)
		bias_gradients = neuron_gradients.sum(axis=1, keepdims=True)
		# Update weights and biases
		self.weights -= learning_rate * weight_gradients
		self.bias -= learning_rate * bias_gradients
		# Update weights and biases for each neuron in the layer
		for i, neuron in enumerate(self.neurons):
			neuron.weights = self.weights[:, i]
			neuron.bias = self.bias[i, 0]
		# Return error gradients for the previous layer
		return np.dot(self.weights.T, neuron_gradients)

class NeuralNetwork:
	def __init__(self, layers, learning_rate=0.1):
		self.layers = layers
		self.learning_rate = learning_rate

	def forward(self, inputs):
		if type(inputs) == list:
			inputs = np.array(inputs)

		for layer in self.layers:
			inputs = layer.forward(inputs)
		return inputs

	def backward(self, inputs, targets, learning_rate):
		# Forward pass
		predictions = self.forward(inputs)

		# Backward pass
		error = predictions - targets
		for layer in reversed(self.layers):
			error = layer.backward(error, inputs, learning_rate)
	
	def train(self, x, y, epochs, learning_rate):
		if type(x) == list:
			x = np.array(x)

		if type(y) == list:
			y = np.array(y)

		for epoch in tqdm(range(epochs), desc="Training neural network"):
			error = 0
			for i in range(len(x)):
				inputs = x[i]
				targets = y[i]

				# Forward pass
				output = self.forward(inputs)

				# Backward pass
				self.backward(inputs, targets, learning_rate)

				# Compute error
				error += np.mean(np.abs(targets - output))

			# Print error at end of epoch
			print(f"Epoch {epoch+1}/{epochs} error: {error/len(x)}")