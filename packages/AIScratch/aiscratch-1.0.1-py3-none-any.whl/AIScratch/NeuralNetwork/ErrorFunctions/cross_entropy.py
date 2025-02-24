from AIScratch.NeuralNetwork.ErrorFunctions import ErrorFunction
import numpy as np

class CrossEntropy(ErrorFunction):
    def __init__(self):
        super().__init__()

    def forward(self, y, y_est):
        y_est = np.clip(y_est, 1e-12, 0.9)  # avoid log 1
        return - y * np.log(y_est)
    
    def backward(self, y, y_est):
        y_est = np.clip(y_est, 1e-12, 1.0)  # avoid div by 0
        return - y / y_est