from AIScratch.NeuralNetwork.ActivationFunctions import ActivationFunction
import numpy as np

class Softmax(ActivationFunction):
    def __init__(self):
        super().__init__("softmax")

    def forward(self, values):
        expZ = np.exp(values - np.max(values, axis=0, keepdims=True))  # numerical stability
        return expZ / np.sum(expZ, axis=0, keepdims=True)

    def backward(self, values): # no backward computation 
        pass

    def weight_initialize(self, n_in = 1, n_out = 1):
        return self._weight_xavier(n_in, n_out)