import math
import random

sigmoid = lambda x: 1 / (1 + math.exp(-x))
derivative = lambda x: sigmoid(x) * (1 - sigmoid(x))

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

class Neuron:
    def __init__(self, inputCount: int) -> None:
	    self.weights = generateNormalDistribution(1, 1, inputCount)
	    self.bias = 0
	    
    def forward(self, inputs: list[int or float]) -> int or float:
	    return sigmoid(sum([w * i for w, i in zip(self.weights, inputs)]))
    
    def backward(self, )