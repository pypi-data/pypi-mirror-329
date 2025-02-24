from AIScratch.NeuralNetwork.Optimizers import Optimizer
import numpy as np

class SGDOptimizer(Optimizer):
    def __init__(self, n_p1, n_p, eta):
        super().__init__()
        self.eta = eta
        self.learning_rates = eta * np.ones(n_p)

    def store(self, grad_L_z, inputs):
        return np.outer(grad_L_z, inputs)

    def optimize(self, grad_L_w, grad_L_b):
        return self.learning_rates, grad_L_w, self.eta * grad_L_b