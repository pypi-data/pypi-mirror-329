from abc import ABC, abstractmethod

class Encoder(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def encode(self, inputs):
        pass

    @abstractmethod
    def decode(self, inputs):
        pass

