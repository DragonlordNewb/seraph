import math
import random

INPUT = "input"
OUTPUT = "output"
HIDDEN = "hidden"

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
        calculation = Value(sigmoid(sum(self.inputValues) / len(self.inputValues)) + self.bias, self)
        self.inputValues = []
        return calculation

    def pump(self) -> None:
        for output in self.outputs:
            self >> output

    def propagateError(self) -> None:
        self.bias -= self.error
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
        self.neurons = []
        for i in range(size):
            self.neurons.append(Neuron())

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

    def pump(self) -> None:
        for neuron in self:
            neuron.pump()

    def propagateError(self) -> None:
        for neuron in self:
            neuron.propagateError()

    def outputs(self) -> list[float]:
        return [neuron.calculate() for neuron in self]

class InputLayer(Layer):
    def __lshift__(self, inputs: list[float]) -> None:
        for neuron in self:
            neuron << inputs

class OutputLayer(Layer):
    def __lshift__(self, reality: list[float]) -> None:
        for neuron, real in zip(self, reality):
            neuron.error = neuron.calculate() - real

class FeedforwardNeuralNetwork:
    def __init__(self, *layers: list[Layer]) -> None:
        self.layers = []

        for index, layer in enumerate(layers):
            if type(layer) == Layer:
                self.layers.append(layer)
            else:
                if index == 0:
                    self.layers.append(InputLayer(layer))
                elif index == len(layers) - 1:
                    self.layers.append(OutputLayer(layer))
                else:
                    self.layers.append(Layer(layer))

        self.axons = []

        for index in range(len(self) - 1):
            for neuron1 in self[index]:
                for neuron2 in self[index + 1]:
                    self.axons.append(Axon(neuron1, neuron2))

    def __repr__(self) -> str:
        return "<seraph.neural.feedforward2.FeedforwardNeuralNetwork containing " + ", ".join([repr(layer) for layer in self]) + ">"

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

    def __getitem__(self, index: int or str or slice) -> Layer or list[Layer]:
        if type(index) == int:
            return self.layers[index]
        elif type(index) == str:
            if index == OUTPUT:
                return self[-1]
            elif index == INPUT:
                return self[0]
            elif index == HIDDEN:
                return self[1:len(self) - 2]
        elif type(index) == slice:
            assert not index.step, "Can't use steps when iterating a FeedforwardNeuralNetwork."
            assert index.start < index.stop, "Bad indices for slicing."
            assert index.start > -1 and index.stop > -1 , "Can't use negative slices on a FeedforwardNeuralNetwork."

            output = []
            for i, layer in enumerate(self):
                if index.start <= i <= index.stop:
                    output.append(layer)

            return output

        raise TypeError("Can only index FeedforwardNeuralNetwork with an integer or slice.")

    def feedforward(self, inputs: list[float]) -> list[float]:
        self[INPUT] << inputs
        for layer in self:
            layer.pump()
        return self[OUTPUT].outputs()

    def backpropagate(self, reality: list[float]) -> None:
        self[OUTPUT] << reality
        for layer in [l for l in self][::-1]:
            layer.propagateError()