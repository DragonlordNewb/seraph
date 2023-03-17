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

import numpy as np # i hate you, numpy, but i'm too lazy to generate my own standard deviations

from seraph import utils

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

class Neuron:
	def __init__(self, inputSize: int, activationFunction: utils.function=sigmoid) -> None:
		self.weights = np.random.randn(inputSize) # because it does the cool standard deviation stuff
		self.bias = 0

		if (not hasattr(self, "activate")) and (activationFunction != None):
			self.activate = activationFunction
		elif hasattr(self, "activate") and (activationFunction != None):
			raise SyntaxError("Cannot both subclass an \"activate\" method and supply one at init.")
		elif (not hasattr(self, "activate")) and (activationFunction == None):
			raise SyntaxError("Must either subclass an \"activate\" method or supply one at init.")

	def __len__(self) -> int:
		return len(self.weights)
		  
	def randomizeWeights(self, inputSize: int=None) -> list[int or float]:
		self.weights = np.random.randn(len(self))

	def feedforward(self, *inputs: list[int]):
		return self.activate(np.dot(np.array(inputs), self.weights) + self.bias)