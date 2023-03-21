# THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE
# PUBLIC LICENSE ("AGREEMENT"). ANY USE, REPRODUCTION OR DISTRIBUTION
# OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT.

import random
from typing import Union
import warnings
import math
from seraph import utils

UNKNOWN = 0
DELTA = "DELTA"
ABSOLUTE = "ABSOLUTE"
ACTION = "ACTION"
REACTION = "REACTION"
SEQBREAK = "SEQBREAK"
ACTIVATION = "activation"
DERIVATIVE = "derivative"
LOSS = "loss"
GRADIENT = "gradient"

def plusOrMinus(x: int, n: int) -> int:
    return x + random.randint(-n, n)

class UnsafeValueWarning(Warning):
    pass

def levenshtein(a, b):
    if len(b) == 0:
        return len(a)
    if len(a) == 0:
        return len(b)

    if len(a) == len(b):
        return levenshtein(a[1:], b[1:])

    return 1 + min([
        levenshtein(a, b[1:]),
        levenshtein(a[1:], b),
        levenshtein(a[1:], b[1:])
    ])

class ActivationFunction:
	def __init__(self, activation: Union[utils.function, None]=None, derivative: Union[utils.function, None]=None) -> None:
		if activation != None:
			self.activation = activation
		if derivative != None:
			self.derivative = derivative
		assert hasattr(self, "activation"), "Must subclass a \"activation(self, x)\" method onto ActivationFunction class."
		assert hasattr(self, "derivative"), "Must subclass a \"derivative(self, x)\" method onto ActivationFunction class."
		assert type(self(ACTIVATION, [1, 0])[0]) in [int, float], "Activation function must return an int or float, not " + type(self(ACTIVATION, [1, 0])).__name__ + "."
		assert type(self(DERIVATIVE, [1, 0])[0]) in [int, float], "Derivative function must return an int or float."
		
	def __repr__(self) -> str:
		return "<seraph.ActivationFunction " + self.__name__ + ">"
	
	def __call__(self, mode: ACTIVATION or DERIVATIVE, x: Union[int, float]) -> Union[int, float]:
		if mode == ACTIVATION:
			if type(x) == list:
				return [self(ACTIVATION, y) for y in x]
			return self.activation(x)
		elif mode == DERIVATIVE:
			if type(x) == list:
				return [self(DERIVATIVE, y) for y in x]
			return self.derivative(x)
		
		
class LossFunction:
	def __init__(self, loss=None, gradient=None) -> None:
		if loss != None:
			self.loss = loss
		if gradient != None:
			self.gradient = gradient
		assert hasattr(self, "loss"), "Must subclass a \"loss(self, reality, prediction)\" method onto ActivationFunction class."
		assert hasattr(self, "gradient"), "Must subclass a \"gradient(self, reality)\" method onto ActivationFunction class."
		assert type(self(LOSS, [1, 0], [0, 1])) in [int, float], "Loss function must return an int or float."
		assert type(self(GRADIENT, [1, 0])[0]) in [int, float], "Loss function gradient must return an int or float."

	def __repr__(self) -> str:
		return "<seraph.LossFunction " + self.__name__ + ">"
	
	def __call__(self, mode: ACTIVATION or DERIVATIVE, x: Union[int, float], y: Union[int or float]=None) -> Union[int, float]:
		if mode == LOSS:
			return self.loss(x, y)
		elif mode == GRADIENT:
			return self.gradient(x)
		raise SyntaxError("\"mode\" argument of calling an LossFunction must be GRADIENT or LOSS.")

	def gradient(self, reality, scale: int=0.1):
		length = len(reality)
		output = [0] * length
		for index in range(length):
			vect1 = vect2 = [0] * length
			vect1[index] = scale
			vect2[index] = -scale
			delta = self.loss(reality, vect1) - self.loss(reality, vect2)
			delta /= 2 * scale
			output[index] = delta
		return output
	
class Sigmoid(ActivationFunction):
	def activation(self, x):
		return 1 / (1 + math.exp(-x))

	def derivative(self, x):
		return self.activation(x) * (1 - self.activation(x))

class MeanSquareError(LossFunction):
	def loss(self, reality, prediction):
		assert len(reality) == len(prediction), "Can't compare reality and prediction arguments of different length (reality == " + str(len(reality)) + " != prediction == " + str(len(prediction)) + ")."
		return sum([(p - r) ** 2 for r, p in zip(reality, prediction)]) / len(reality)

		raise SyntaxError("\"mode\" argument of calling an ActivationFunction must be ACTIVATION or DERIVATIVE.")
