from abc import ABC, abstractmethod
from typing import Callable
from AIScratch.NeuralNetwork.Optimizers import Optimizer
from AIScratch.NeuralNetwork.ActivationFunctions import ActivationFunction

class SpatialLayer(ABC):
    def __init__(self, k, padding, stride, channel_out, activation_function, name):
        self.k : int = k
        self.padding : int = padding
        self.stride : int = stride
        self.channel_out : int = channel_out
        self.activation_function : ActivationFunction = activation_function
        self.optimizer : Optimizer = None
        self.last_sums : list[float] = None
        self.last_activations : list[float] = None
        self.filters : list[list[float]] = []
        self.bias : list[float] = []
        self.name = name
        self.is_spatial = True
    
    @abstractmethod
    def _initialize(self, n_in, optimizer_factory : Callable[[int, int], Optimizer], list_of_filters = None):
        pass
    
    @abstractmethod
    def forward(self, inputs, is_training = False):
        pass

    @abstractmethod
    def propagation(self, grad_L_z):
        pass

    @abstractmethod
    def store(self, grad_L_z):
        pass

    @abstractmethod
    def backward(self):
        pass

