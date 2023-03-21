import numpy as np
from typing import Union
import math

from seraph.common import ActivationFunction

class Sigmoid(ActivationFunction):
	def activation(self, x):
		return 1 / (1 + math.exp(-x))

	def derivative(self, x):
		return self.activation(x) * (1 - self.activation(x))

class Neuron:
    inputs = []
    output = 0
    weights = []
    index = 0
    bias = 0

    def __repr__(self) -> str:
        return "<seraph.neural.crystalline.Neuron>"
    
    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Union[int or float]:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self[self.n]

    def __getitem__(self, index: int) -> Union[int or float]:
        return self.weights[index]

    def __lshift__(self, inputs: list[Union[int or float]]) -> list[Union[int or float]]:
        self.inputs = inputs
        return [(i * w) + self.bias for i, w in zip(inputs, self.weights)]

    def configure(self, size: int, index: int, mu: int, sigma: int) -> None:
        self.weights = list(np.random.normal(mu, sigma, size))
        self.index = index
        self.weights[self.index] = None

class CrystallineNeuralNetwork:
    def __init__(self, size: int=100, mu: int=1, sigma: int=0.1) -> None:
        self.neurons = [Neuron() for _ in range(size)]

        for index, neuron in enumerate(self):
            neuron.configure(size, index, mu, sigma)

    def __repr__(self) -> str
