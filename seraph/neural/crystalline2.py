import math
import os
from typing import Union

COMPUTATION = "computation"
ADJUSTMENTS = "adjustments"

BadModeError = RuntimeError("Neuron mode must be either \"computation\" or \"adjustments\".")

def sigmoid(x):
    if type(x) == list:
        return [sigmoid(y) for y in x]
    return 1 / (1 + math.exp(-x))

class Neuron:
    bias = 0
    inputs = []
    output = None
    outputGenerated = False
    inputCount = 0
    accumulatedError = 0

    inputAxons = []
    outputAxons = []

    mode = COMPUTATION

    def __init__(self) -> None:
        self.id = os.urandom(256)

    def __repr__(self) -> str:
        return "<seraph.neural.crystalline2.Neuron with " + str(len(self)) + "inputs>"

    def __len__(self) -> int:
        return self.inputCount

    def __eq__(self, other: object) -> bool:
        if type(other) != Neuron:
            return False
        return self.id == other.id

    def __div__(self, mode: COMPUTATION or ADJUSTMENTS) -> None:
        self.wipe()
        if mode not in [COMPUTATION, ADJUSTMENTS]:
            raise BadModeError
        self.mode = mode
        for axon in self.inputAxons:
            axon / mode
        for axon in self.outputAxons:
            axon / mode

    def __lshift__(self, value: int) -> Union[int, float]:
        if self.mode == COMPUTATION:
            self.inputs.append(value)
            return len(self)
        elif self.mode == ADJUSTMENTS:
            self.accumulatedError += value
            return self.accumulatedError
        else:
            raise BadModeError

    def __rshift__(self, axon: object) -> Union[int, float]:
        if self.mode == COMPUTATION:
            if not self.output:
                val = self.calculate()
            else:
                val = self.output
            axon << val + bias
            return val + bias
        elif self.mode == ADJUSTMENTS:
            axon << self.accumulatedError
            return self.accumulatedError

    def adjust(self) -> Union[int, float]:
        self.bias -= self.accumulatedError / self.averageOutputWeight()
        return self.bias

    def averageOutputWeight(self) -> Union[int, float]:
        return sum([axon.weight for axon in self.outputAxons]) / len(self.outputAxons)

    def averageInputWeight(self) -> Union[int, float]:
        return sum([axon.weight for axon in self.inputAxons])/ len(self.inputAxons)

    def pump(self) -> None:
        if self.mode == COMPUTATION:
            axons = self.outputAxons
        elif self.mode == ADJUSTMENTS:
            axons = self.inputAxons
        
        for axon in axons:
            self >> axon

    def wipe(self) -> None:
        self.output = None
        self.outputGenerated = False
        self.inputs = []
        self.accumulatedError = 0

class Axon:
    mode = COMPUTATION
    weight = (random.random() - 0.5) * 2

    def __init__(self, front: Neuron, back: Neuron) -> None:
        self.front = front
        self.back = back

        if self not in self.front.outputAxons:
            self.front.outputAxons.append(self)
        if self not in self.back.inputAxons:
            self.back.inputAxons.append(self)

    def __div__(self, mode: COMPUTATION or ADJUSTMENTS) -> None:
        if mode not in [COMPUTATION, ADJUSTMENTS]:
            raise BadModeError
        self.mode = mode

    def __lshift__(self, value: Union[int, float]) -> None:
        if self.mode == COMPUTATION:
            self.back << value * self.weight
        elif self.mode == ADJUSTMENTS:
            self.front << value * self.weight
            self.weight /= value

class CrystallineNeuralNetwork:
    axons = []

    def __init__(self, size: int=100) -> None:
        self.neurons = [Neuron() for _ in range(size)]
        self.size = size

        for neuron in self:
            for otherNeuron in self - neuron:
                self.axons.append(Axon(neuron, otherNeuron))

        self / COMPUTATION

    def __repr__(self) -> str:
        return "<seraph.neural.crystalline2.CrystallineNeuralNetwork with " + str(len(self)) + " neurons>"

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> object:
        self.n = -1
        return self

    def __next__(self) -> Neuron:
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self[self.n]

    def __getitem__(self, index: int) -> Neuron:
        return self.neurons[index]

    def __div__(self, mode: COMPUTATION or ADJUSTMENTS) -> None:
        for neuron in self:
            neuron / mode

    def __sub__(self, neuron: Neuron) -> list[Neuron]:
        return [n for n in self if n != Neuron]

    def __lshift__(self, inputs: list[Union[int, float]]) -> None:
        for neuron, inp in zip(self, inputs):
            neuron << inp

    def adjust(self) -> None:
        for neuron in self:
            neuron.adjust()

    def backpropagate(self, reality: list[Union[int, float]], iterations: int=1) -> None:
        self / ADJUSTMENTS
        for neuron in self:
            neuron.accumulatedError = neuron.output - reality
        for iteration in range(iterations):
            self.pump()
            self.adjust()

    def biases(self) -> list[Union[int, float]]:
        return [neuron.bias for neuron in self]

    def calculate(self) -> None:
        for neuron in self:
            neuron.calculate()

    def predict(self, inputs: list[Union[int, float]], iterations: int=1):
        self / COMPUTATION
        self << inputs
        for iteration in range(iterations):
            self.calculate()
            self.resetInputs()
            self.pump()
        return [neuron.output for neuron in self]

    def pump(self) -> None:
        for neuron in self:
            neuron.pump()

    def resetInputs(self) -> None:
        for neuron in self:
            neuron.inputs = []

    def adapt(self, inputs: list[Union[int, float]], reality: list[Union[int, float]], epochs: int=1000) -> None:

    def weights(self) -> list[Union[int, float]]:
        return [axon.weight for axon in self.axons]

    def wipe(self):
        for neuron in self:
            neuron.wipe()