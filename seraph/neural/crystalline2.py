import math

def sigmoid(x):
    if type(x) == list:
        return [sigmoid(y) for y in x]
    return 1 / (1 + math.exp(-x))

class Neuron:
    self