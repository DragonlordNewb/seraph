import math
import random

FEEDFORWARD = "feedforward"
BACKPROPAGATION = "backpropagation"

BAD_MODE = RuntimeError("Mode must be \"feedforward\" or \"backpropagation\".")

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class Value:
    def __init__(self, value: any, origin: object) -> None:
        self.value = value
        self.origin = origin

class Neuron:
    inputs = []
    outputs = []

    inputValues = []

    error = 0

    def __init__(self) -> None:
        self.id = random.randbytes(64)
        self.bias = random.random()

    def __repr__(self) -> str:
        return "<seraph.neural.feedforward2.Neuron>"

    def __eq__(self, other: object) -> bool:
        if type(other) == Neuron:
            return self.id == other.id
        return False

    def __lshift__(self, value: Value) -> None:
        if value.origin in self.inputs:
            self.inputValues.append(value)
        else:
            self.error += value

    def __rshift__(self, obj: object) -> None:
        if obj in self.outputs:
            obj << self.calculate()
        elif obj in self.inputs:
            obj << Value(self.error, self)

    def calculate(self) -> float:
        calculation = Value(sigmoid(sum(self.inputValues) / len(self.inputValues)), self)
        self.inputValues = []
        return calculation

    def pump(self) -> None:
        for output in self.outputs:
            self >> output

    def propagateError(self) -> None:
        for inp in self.inputs:
            self >> inp

class Axon:
    def __init__(self, front: Neuron, back: Neuron) -> None:
        self.front = front
        self.front.outputs.append(self)
        self.back = back
        self.back.inputs.append(self)
        self.weight = random.random()

    def __lshift__(self, value: Value) -> None:
        if value.origin == self.front:
            self.back << Value(value.value * self.weight, self)
        elif value.origin == self.back:
            self.front << Value(value.value * self.weight, self)
            self.weight /= value.value

class Layer:
    def __init__(self, size: int=5) -> None:
        self.neurons = [Neuron() for _ in range(size)]

    def __repr__(self) -> str:
        return "<seraph.neural.feedforward2.Layer with " + str(len(self)) + " neurons>"

    def __len__(self) -> int:
        return len(self.neurons)

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Neuron:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.neurons[self.n]

    def __lshift__(self, inputs: list[float]) -> None:
        for neuron in self:
            neuron << inputs

    def pump(self) -> None:
        for neuron in self:
            neuron.pump()

    def propagateError(self) -> None:
        for neuron in self:
            neuron.propagateError()