from AIScratch.NeuralNetwork.ActivationFunctions import ActivationFunction
import numpy as np
class Treshold(ActivationFunction):
    def __init__(self, up = 1, down = 0):
        super().__init__("treshold")
        self.up = up
        self.down = down

    def forward(self, value):
        return np.where(value < 0, self.down, self.up)
    
    def backward(self, value):
        return np.ones_like(value) # not real derivative but works fine

    def weight_initialize(self, n_in = 1, n_out = 1):
        return self._weight_uniform(n_in, n_out)