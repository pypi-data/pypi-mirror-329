from abc import ABC, abstractmethod
from typing import Callable
from AIScratch.NeuralNetwork.Perceptron import Perceptron
from AIScratch.NeuralNetwork.Optimizers import Optimizer
from AIScratch.NeuralNetwork.ActivationFunctions import ActivationFunction

class Layer(ABC):
    def __init__(self, n_out, activation_function, name):
        self.n_out : int = n_out
        self.activation_function : ActivationFunction = activation_function
        self.optimizer : Optimizer = None
        self.last_sums : list[float] = None
        self.last_activations : list[float] = None
        self.neurons : list[Perceptron] = []
        self.name = name
        self.is_spatial = False
    
    @abstractmethod
    def _initialize(self, n_in, optimizer_factory : Callable[[int, int], Optimizer], list_of_weights = []):
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

