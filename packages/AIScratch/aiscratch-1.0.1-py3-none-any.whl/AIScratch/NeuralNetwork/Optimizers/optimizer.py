from abc import ABC, abstractmethod

class Optimizer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def store(self, grad_L_z, inputs):
        pass

    @abstractmethod
    def optimize(self, grad_L_w, grad_L_b):
        pass