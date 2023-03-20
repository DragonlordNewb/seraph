from typing import Union

from seraph import utils

ACTIVATION = "activation"
DERIVATIVE = "derivative

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
		return "<seraph.ActivationFunction>"
	
	def __call__(self, mode: ACTIVATION or DERIVATIVE, x: Union[int, float]) -> Union[int, float]:
		if mode == ACTIVATION:
			return self.activation(x)
		elif mode == DERIVATIVE:
			return self.derivative(x)
		raise SyntaxError("\"mode\" argument of calling an ActivationFunction must be ACTIVATION or DERIVATIVE."
		
class Neuron:
	def __init__(self, activation: ActivationFunction) -> None:
		self.inputs = []
		self.outputs = []
		self.inputAxons = []
		self.outputAxons = []
		
		self.activation = activation
		
	def __lshift__(self, value: Union[int, float]) -> list[Union[int, float]]:
		self.inputs.append(

class Axon:
	def __init__(self, weight, front: object, back: object) -> None:
		self.weight = weight
		self.front = front
		self.back = back
		
	def __repr__(self) -> str:
		return "<Axon from " + repr(self.front) + " to " + repr(self.back) + ">"
	
	def __lshift__(self, value: Union[int, float]) -> Union[int, float]:
		throughput = value * self.weight
		self.back << throughput
		return throughput
