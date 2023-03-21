import numpy as np
from typing import Union
import math

from seraph.common import ActivationFunction, LossFunction, Sigmoid

ACTIVATION = "activation"
DERIVATIVE = "derivative"
LOSS = "loss"
GRADIENT = "gradient"

class MeanSquareError(LossFunction):
    def loss(self, prediction, reality):
        return (prediction - reality) ** 2

class Neuron:
    inputs = []
    outputs = []
    weights = []
    index = 0
    bias = 0

    def __init__(self, activation: ActivationFunction=Sigmoid(), loss: LossFunction=MeanSquareError()):
        self.activation = activation
        self.loss = loss

    def __repr__(self) -> str:
        return "<seraph.neural.crystalline.Neuron>"

    def __len__(self) -> int:
        return len(self.weights)
    
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
        self.output = []
        for i, w in zip(inputs, self):
            if w != None:
                self.output.append(self.activation(ACTIVATION, i * w))
            else:
                self.output.append(None)
        return self.output

    def configure(self, size: int, index: int, mu: int, sigma: int) -> None:
        self.weights = list(np.random.normal(mu, sigma, size))
        self.index = index
        self.weights[self.index] = None

    def calculateError(self, reality):
        return self.loss(LOSS, self.outputs, reality)

class CrystallineNeuralNetwork:
    inputs = []
    outputs = []

    def __init__(self, activation: ActivationFunction=Sigmoid(), loss: LossFunction=MeanSquareError(), size: int=100, mu: int=1, sigma: int=0.1) -> None:
        self.neurons = [Neuron(activation, loss) for _ in range(size)]

        for index, neuron in enumerate(self):
            neuron.configure(size, index, mu, sigma)

    def __len__(self) -> int:
        return len(self.neurons)

    def __repr__(self) -> str:
        return "<seraph.neural.crystalline.CrystallineNeuralNetwork of size " + str(len(self)) + ">"

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

    def transform(self, inputs: list[Union[int or float]], epochs: int=1) -> list[Union[int, float]]:
        assert len(inputs) == len(self), "Must feed exactly one input to each neuron."

        # Sometime, you should write out an explanation for the "rotosum matrix transform".

        for epoch in range(epochs):
            outputs = [neuron << inputs for neuron in self]
            inputs = []
            for index in range(len(outputs)):
                ix = 0
                for output in outputs:
                    ix += output[index]
                inputs.append(ix)
        
        return inputs

    def feedback(self, reality: list[Union[int, float]], adjustment: int=1) -> None:
        assert len(reality) == len(self), "Must feed exactly one reality element to each neuron (len(reality) != len(crystal))"

        errors = [neuron.calculateError(real) for neuron, real in zip(self, reality)]
        adjustedErrors = errors

        for epoch in range(adjustment):
            newError = []
            for neuron in self:
                outputtedErrors = []
                for otherNeuron in self:
                    if neuron.index == otherNeuron.index:
                        outputtedErrors.append(None)
                    else:
                        outputtedErrors.append(adjustedErrors[otherNeuron.index])

                newError.append(math.sqrt(sum([
                    (outputtedErrors[index] * neuron.weights[index]) ** 2 \
                    for index in range(len(neuron)) \
                    if outputtedErrors[index] != None and neuron.weights[index] != None
                ])))

            adjustedError = newError

