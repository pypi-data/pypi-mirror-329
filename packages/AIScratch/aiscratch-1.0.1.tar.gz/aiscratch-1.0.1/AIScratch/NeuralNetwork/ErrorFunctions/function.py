from abc import ABC, abstractmethod

class ErrorFunction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def forward(self, y : float, y_est : float) -> float:
        pass

    @abstractmethod
    def backward(self, y : float, y_est : float) -> float:
        pass