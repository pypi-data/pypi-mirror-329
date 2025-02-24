from AIScratch.NeuralNetwork.ActivationFunctions import ActivationFunction
import numpy as np

class ReLU(ActivationFunction):
    def __init__(self, treshold = 0, slope = 1):
        super().__init__("relu")
        self.treshold = treshold
        self.slope = slope

    def forward(self, value):
        value = np.asarray(value)  # Convertit en np.array si ce n'est pas déjà le cas
        return np.where(value <= self.treshold, 0, self.slope * value)

    def backward(self, value):
        value = np.asarray(value)
        return np.where(value <= self.treshold, 0, self.slope)

    def weight_initialize(self, n_in = 1, n_out = 1):
        return self._weight_he(n_in, n_out)