from AIScratch.NeuralNetwork.ErrorFunctions import ErrorFunction
import numpy as np

class HingeLoss(ErrorFunction):
    def __init__(self):
        super().__init__()

    def forward(self, y, y_est):
        tmp = 1 - y * y_est
        return np.where(tmp < 0, 0, tmp)
    
    def backward(self, y, y_est):
        tmp = 1 - y * y_est
        if tmp <= 0:
            return 0
        return np.where(tmp < 0, 0, -y)