def	test_00():
	print("Seraph system is wired up.")
				
def	test_01():
	from seraph import neural
				
	net = neural.NeuralNetwork([
		neural.Layer(3, 3),
		neural.Layer(3, 3),
		neural.Layer(3, 3)
	])

	net.train([0, 1, 2, 3, 4], [0, 2, 4, 6, 8], 1000, 0.01)

	net.forward([0, 1, 2, 3, 4])