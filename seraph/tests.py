def	test_00():
	print("Seraph system is wired up.")
				
def	test_01():
	import numpy as np

	from seraph import neural_base

	x = [i for i in range(50)]
	y = [2 * X + 1 for X in x]

	# Create a neural net with 2 input neurons, 2 hidden neurons, and 1 output neuron
	input_layer = neural_base.InputLayer([neural_base.Neuron(1), neural_base.Neuron(1)])
	hidden_layer = neural_base.Layer([neural_base.Neuron(2) for _ in range(2)])
	output_layer = neural_base.OutputLayer([neural_base.Neuron(2)])

	# input_layer.nextLayer = hidden_layer
	# hidden_layer.nextLayer = output_layer

	nn = neural_base.NeuralNetwork([input_layer, hidden_layer, output_layer])

	# Train the neural net using the generated data
	nn.train(x, y, epochs=1000, learning_rate=1)

	# Test the neural net using the test data
	y_pred = nn.feedforward(5)
	print("Predicted Output:")
	print(y_pred)
	print("Expected Output:")
	print(y)

def test_02():
	from seraph import neural1

	x = [[i] for i in range(50)]
	y = []
	for X in x:
		val = (2 * X[0]) + 1
		y.append([val])

	schem = neural1.NeuralNetworkSchematic(1, [3, 5, 5, 5, 5, 5, 2])
	nn = schem.assemble()
	nn.train(x, y)
	print(nn.predict([5]))
	print(nn.predict([6]))
	print(nn.predict([7]))

def test_03():
	from seraph.neural import feedforward2 as ff 

	nn = ff.FeedforwardNeuralNetwork(3, 5, 5, 5, 5, 5, 3)

def test_04():
	from seraph.neural import crystalline4
	c = crystalline4.NeuralCrystal()
	inp = ([0, 1] * 12) + [0]
	out = ([0, 1] * 12) + [1]
	print(c.transform(inp, 5))
	print()
	x = c.train([inp], [out], 5)
	print(c.transform(inp, 5))
	print()
	print(x)