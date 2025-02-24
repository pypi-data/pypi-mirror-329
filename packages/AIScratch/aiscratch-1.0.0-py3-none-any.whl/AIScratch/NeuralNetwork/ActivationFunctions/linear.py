from AIScratch.NeuralNetwork.ActivationFunctions import ActivationFunction

class Linear(ActivationFunction):
    def __init__(self, origin = 0, slope = 1):
        super().__init__("linear")
        self.origin = origin
        self.slope = slope

    def forward(self, value):
        return self.slope * value + self.origin

    def backward(self, value):
        return self.slope

    def weight_initialize(self, n_in = 1, n_out = 1):
        return self._weight_he(n_in, n_out)