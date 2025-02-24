from abc import ABC, abstractmethod
import random
import numpy as np

class ActivationFunction(ABC):
    def __init__(self, name):
        self.name = name
        pass

    @abstractmethod
    def forward(self, value : float) -> float:
        pass

    @abstractmethod
    def backward(self, value) -> float:
        pass

    def _weight_uniform(self, n_in, n_out):
        return random.random() * 2 - 1
    
    def _weight_he(self, n_in, n_out):
        return np.random.normal(0, 2 / n_in)

    def _weight_xavier(self, n_in, n_out):
        bound = 6 ** 0.5 / (n_in + n_out) ** 0.5
        return random.random() * 2 * bound - bound

    @abstractmethod
    def weight_initialize(self, n_in = 1, n_out = 1) -> float:
        pass