import numpy as np


class NeuralNetwork():
    def __init__(self, num_inputs, hidden_layers):
        self.weights = []
        prev_size = num_inputs + 1
        for layer in hidden_layers:
            self.weights.append(np.random.rand(layer, prev_size) * 2 - 1)
            prev_size = layer + 1
        self.weights.append(np.random.rand(prev_size) * 2 - 1)

    def evaluate(self, input):
        for w in self.weights:
            input = np.tanh(w @ np.append(input, [1]))
        return input
