# THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE
# PUBLIC LICENSE ("AGREEMENT"). ANY USE, REPRODUCTION OR DISTRIBUTION
# OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT.

import random
import warnings

UNKNOWN = 0
DELTA = "DELTA"
ABSOLUTE = "ABSOLUTE"
ACTION = "ACTION"
REACTION = "REACTION"
SEQBREAK = "SEQBREAK"

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
		assert type(self(ACTIVATION, [1, 0])) in [int, float], "Activation function must return an int or float."
		assert type(self(DERIVATIVE, [1, 0])) in [int, float], "Derivative function must return an int or float."
		
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
		raise SyntaxError("\"mode\" argument of calling an ActivationFunction must be ACTIVATION or DERIVATIVE.")
