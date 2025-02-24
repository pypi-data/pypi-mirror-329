import numpy as np

class Perceptron():
    def __init__(self, weights, bias = 0):
        self.weights = np.array(weights)
        self.bias = bias
    
    def forward(self, inputs):# store for learning  
        return np.dot(inputs, self.weights) + self.bias
    
    def backward(self, learning_rates, weighted_errors, biais_update):
        self.weights -= learning_rates * weighted_errors
        self.bias -= biais_update

