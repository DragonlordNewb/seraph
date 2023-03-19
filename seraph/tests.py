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
	from seraph import neural

	x = [i for i in range(50)]
	y = [2 * X + 1 for X in x]

	nn = neural.NeuralNetwork(
		neural.Layer(neural.Neuron(1), neural.Neuron(1), neural.Neuron(1)),
		neural.Layer(neural.Neuron(3), neural.Neuron(3), neural.Neuron(3), neural.Neuron(3), neural.Neuron(3)),
		neural.Layer(neural.Neuron(5), neural.Neuron(5), neural.Neuron(5), neural.Neuron(5), neural.Neuron(5)),
		neural.Layer(neural.Neuron(5), neural.Neuron(5), neural.Neuron(5), neural.Neuron(5), neural.Neuron(5)),
		neural.Layer(neural.Neuron(5), neural.Neuron(5), neural.Neuron(5), neural.Neuron(5), neural.Neuron(5)),
		neural.Layer(neural.Neuron(5), neural.Neuron(5), neural.Neuron(5), neural.Neuron(5), neural.Neuron(5)),
		neural.Layer(neural.Neuron(5), neural.Neuron(5), neural.Neuron(5)),
	)