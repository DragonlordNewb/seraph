import random

COMPUTE = "compute"
ADJUST = "adjust"

cid = -1
def getID():
    """
    Generate a random unique ID to be used internally.
    """
    global cid

    cid += 1
    return cid

class Value:
    """
    A wrapper for arbitrary values that allows the origin
    of the value to be tracked.
    """
    def __init__(self, origin: object, value: float) -> None:
        self.origin = origin
        self.value = value

    def __repr__(self):
        return "<Value " + repr(self.value) + " from " + repr(self.origin) + ">"

    def __invert__(self):
        return self.value

class Neuron:
    """
    The core of the module.
    """

    inputs = []
    outputs = []
    calculation = 0
    bias = random.random()
    accumulatedError = 0

    def __init__(self, parentNeuralNetwork: object) -> None:
        self.parent = parentNeuralNetwork
        self.id = getID()

    def __repr__(self) -> str:
        return "<seraph.neural.crystalline3.Neuron id=" + str(self.id) + ">"
    
    def __eq__(self, obj: object) -> bool:
        if type(obj) != Neuron:
            return False
        return self.id == obj.id

    def __lshift__(self, value: Value) -> None:
        if value.origin in self.inputs:
            self.

    def pump(self, value: float, mode: COMPUTE or ADJUST=COMPUTE):
        if mode == COMPUTE:
            axons = self.outputs
        elif mode == ADJUST:
            axons = self.inputs
        for axon in axons:
            axon << Value(self, value)

    def 
    
class Axon:
    """
    Connects Neurons together.
    """
    weight = random.random()
    def __init__(self, front: Neuron, back: Neuron) -> None:
        self.front = front
        self.front.outputs.append(self)
        self.back = back
        self.back.inputs.append(self)

    def __repr__(self) -> str:
        return "<seraph.neural.crystalline3.Axon connecting " + repr(self.front) + " to " + repr(self.back) + ">"

    def __lshift__(self, value: Value) -> None:
        if value.origin == self.front:
            self.back << Value((~value) * self.weight)
        elif value.origin == self.back:
            self.front << Value((~value) * self.weight)
