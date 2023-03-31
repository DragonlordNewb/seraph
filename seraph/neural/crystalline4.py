from typing import Union
from random import random
from math import exp

FEEDFORWARD = "feedforward"
BACKPROPAGATION = "backpropagation"
LEARNING_RATE = 0.01

def sigmoid(x):
    return 1 / (1 + exp(-x))

class Neuron:
    """
    The Neuron object for the Crystalline Neural Networks.
    
    Accepts an optional "bias" parameter that allows the manual
    control of the neuron's bias. The bias defaults to a random
    value between 0 and 1, exclusive.
    """

    def __init__(self, bias: Union[float, int, None]=None) -> None:
        self.inputAxons: list[Axon] = []
        self.outputAxons: list[Axon] = []
        self.inputs: list[float] = []
        self.output: float = 0
        self.bias: Union[float, int] = bias or random()
        self.mode = FEEDFORWARD

    def __repr__(self) -> str:
        """Representation function."""
        return "<seraph.neural.crystalline4.Neuron bias=" + str(self.bias) + " in " + self.mode + " mode>"

    def __lshift__(self, value: Union[float, int]) -> None:
        """Feed data into the Neuron."""
        self.inputs.append(value)

    def __rshift__(self, value: Union[float, int, None]) -> None:
        """Cause the Neuron to pump data through its output Axons."""
        if self.mode == FEEDFORWARD:
            axons = self.outputAxons
        elif self.mode == BACKPROPAGATION:
            axons = self.inputAxons
        else:
            raise RuntimeError("Bad mode " + str(self.mode) + ".")
        value = value or self.output
        for axon in axons:
            axon << (value, self)
            self.bias -= value * LEARNING_RATE

    def __mod__(self, expected: Union[float, int]) -> Union[float, int]:
        """Compute the neuron's error."""
        return self.output - expected

    def __invert__(self) -> None:
        """Compute the neuron's output value."""
        self.output = sigmoid(sum(self.inputs) + self.bias)

    def __matmul__(self, mode: Union[str, None]) -> None:
        """Set the neuron's mode."""
        if mode == None:
            if self.mode == BACKPROPAGATION:
                self.mode = FEEDFORWARD
            elif self.mode == FEEDFORWARD:
                self.mode == BACKPROPAGATION
            else:
                raise RuntimeError("Bad mode " + str(self.mode) + ".")
        elif mode == BACKPROPAGATION:
            self.mode = BACKPROPAGATION
        elif mode == FEEDFORWARD:
            self.mode = FEEDFORWARD
        else:
            raise RuntimeError("Bad mode " + str(self.mode) + ".")

    def clear(self) -> None:
        """Wipe the inputs."""
        self.inputs = []

class Axon:
    """
    The Axon object that links together Neurons.

    Accepts "front", "back", and "weight" parameters. The front
    neuron is the neuron that the Axon receives data from during
    the feedforward phase; the back neuron is the neuron that 
    receives these data. Likewise, during backpropagation, the
    Axon receives data from the back Neuron and sends it to the
    front Neuron. The "weight" parameter allows manual control of
    the Axon's weight, which is defaulted to a random.
    """

    def __init__(self, front: Neuron, back: Neuron, weight: Union[int, float, None]=None) -> None:
        self.front: Neuron = front
        self.back: Neuron = back
        self.weight: Union[int, float] = weight or random()

        if self not in self.front.outputAxons:
            self.front.outputAxons.append(self)
        if self not in self.back.inputAxons:
            self.front.inputAxons.append(self)

    def __repr__(self) -> str:
        """Representation function."""
        return "<seraph.neural.crystalline4.Axon " + repr(self.front) + " to " + repr(self.back) + ">"

    def __lshift__(self, package: tuple[Union[int, float], Neuron]) -> None:
        """Run data through the Axon."""
        value, origin = package
        if origin == self.front:
            self.back << value * self.weight
        elif origin == self.back:
            self.front << value * self.weight
            self.weight -= value * LEARNING_RATE * self.weight
        else:
            raise RuntimeError("Origin must be the front or back of the Axon.")

class NeuralCrystal:
    """
    The crystalline neural network you're looking for.

    Accepts a list of neurons or an integer in the "structure" parameter,
    which defaults to 25. These are either the neurons of the network
    or the number of random neurons to be generated.
    """

    def __init__(self, structure: Union[list[Neuron], int]=25) -> None:
        if type(structure) == int:
            self.neurons = []
            for _ in range(structure):
                self.neurons.append(Neuron())

        elif type(structure) == list:
            self.neurons = structure

        axons = []
        for neuron in self:
            for otherNeuron in self:
                axons.append(Axon(neuron, otherNeuron))

    def __repr__(self) -> str:
        """Representation function."""
        return "<seraph.neural.crystalline4.NeuralCrystal of size " + str(len(self)) + ">"

    def __len__(self) -> int:
        """Evaluate the number of neurons in the crystal."""
        return len(self.neurons)
        
    def __iter__(self) -> object:
        """Set up iteration."""
        self.n = -1
        return self

    def __next__(self) -> Neuron:
        """Iterate."""
        self.n += 1
        if self.n >= len(self):
            raise StopIteration
        return self.neurons[self.n]

    def __matmul__(self, mode: Union[str, None]) -> None:
        for neuron in self:
            neuron @ mode

    def __lshift__(self, values: list[Union[int, float]]) -> None:
        """Feed data into the crystal."""
        for neuron in self:
            for value in values:
                neuron << value

    def __or__(self, iterations: int=1) -> list[Union[int, float]]:
        """Transform the data that's been fed in."""
        self @ FEEDFORWARD

        for neuron in self:
            ~neuron
        for _ in range(iterations):
            for neuron in self:
                neuron >> None
            for neuron in self:
                ~neuron
                neuron.clear()
        return [neuron.output for neuron in self]

    def __rshift__(self, expected: list[Union[int, float]]) -> list[Union[int, float]]:
        """Backpropagate error."""
        self @ BACKPROPAGATION

        errors = []

        for neuron, value in zip(self, expected):
            error = neuron % value
            neuron >> error
            errors.append(error)

        return errors

    def transform(self, inputs: list[Union[int, float]], iterations: int=1) -> list[Union[int, float]]:
        """Transform the data (higher level function)."""
        self.clear()
        self << inputs
        return self | iterations

    def learn(self, inputs: list[Union[int, float]], expected: list[Union[int, float]], iterations: int=1) -> Union[int, float]:
        """Learn from mistakes and return the factor of improvement."""
        self.clear()
        self << inputs
        self | iterations
        initialErrors = self >> expected
        improvedErrors = [neuron % value for neuron, value in zip(self, expected)]
        return sum([initialError - improvedError for initialError, improvedError in zip(initialErrors, improvedErrors)])

    def train(self, 
             inputDataset: list[list[Union[int, float]]], 
             expectedDataset: list[list[Union[int, float]]], 
             iterations: int=1, 
             epochs: int=100) -> list[Union[int, float]]:
        """Train the neural crystal on an input and output dataset."""
        errorsOverTime = []
        self.clear()
        for _ in range(epochs):
            for i, o in zip(inputDataset, expectedDataset):
                errorsOverTime.append(self.learn(i, o, iterations))

        return errorsOverTime

    def clear(self) -> None:
        """Clear the network."""
        for neuron in self:
            neuron.clear()
        