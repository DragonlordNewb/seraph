import random
import math
from typing import Union

class Function:
    def __call__(*args, **kwargs) -> any:
        return self.call(*args, **kwargs)

    def call(self, *args, **kwargs) -> any:
        raise TypeError("Can't use the base Function class.")

class ActivationFunctionDerivative(Function):
    def __init__(self, original: Function) -> None:
        self.original = original

    def __invert__(self):
        return self.original

class ActivationFunction(Function):
    derivative = None

    def __invert__(self):
        return self.derivative(self)

class SigmoidDerivative(ActivationFunctionDerivative):
    def call(x) -> float:
        return (1 / (1 + (math.e ** -x))) * (1 - (1 / (1 + (math.e ** -x))))

class Sigmoid(ActivationFunction):
    derivative = SigmoidDerivative

    def call(x) -> float:
        return (1 / (1 + (math.e ** -x)))

class Neuron:
    def __init__(self, activation: ActivationFunction=Sigmoid) -> None:
        self.bias = random.random()
        self.activation = activation

        self.inputs: list[float]
        self.output: float=0
        self.inputAxons: list[Axon] = []
        self.outputAxons: list[Axon] = []

    def __repr__(self) -> str:
        return "<seraph.neural.feedforward3.Neuron " + str(len(self.inputAxons)) + " to " + str(len(self.outputAxons)) + ">"

    def __lshift__(self, value: float) -> None:
        self.inputs.append(value)

    def __rshift__(self, output: Union[float, None]) -> None:
        for axon in self.outputAxons:
            axon << (output or self.output, self)

    def __invert__(self) -> None:
        self.output = self.activation(sum(self.inputs))

    def __mod__(self, expected: float) -> float:
        return self.output - expected

class Axon:
    def __init__(self, front: Neuron, back: Neuron) -> None:
        self.weight = random.random()

        self.front = front
        self.back = back

    def __repr__(self) -> str:
        return "<seraph.neural.feedforward3.Neuron " + repr(self.front) + " to " + repr(self.back) + ">"

    def __lshift__(self, package: tuple[float, Neuron]) -> None:
        value, origin = package
        if origin == self.front:
            self.back << value * self.weight
        elif origin == self.back:
            self.front << value * self.weight
            self.weight /= value

class Layer:
    def __init__(self, neurons):
        pass