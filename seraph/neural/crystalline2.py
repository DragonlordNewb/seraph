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
        if mode not in [COMPUTATION, ADJUSTMENTS]:
            raise BadModeError
        self.mode = mode

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

    def pump(self) -> None:
        if self.mode == COMPUTATION:
            axons = self.outputAxons
        elif self.mode == ADJUSTMENTS:
            axons = self.inputAxons
        
        for axon in axons:
            self >> axon

class Axon:
    mode = COMPUTATION
    
    def __init__(self, front: Neuron, back: Neuron) -> None:
        self.front = front
        self.back = back

    def __lshift__(self, value: Union[int, float]) -> None

class CrystallineNeuralNetwork:
    axons = []

    def __init__(self, size: int=100) -> None:
        self.neurons = [Neuron() for _ in range(size)]
        self.size = size

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