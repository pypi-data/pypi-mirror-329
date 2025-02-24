from AIScratch.NeuralNetwork.ErrorFunctions import ErrorFunction

class MSE(ErrorFunction):
    def __init__(self):
        super().__init__()

    def forward(self, y, y_est):
        return 0.5 * (y - y_est) * (y - y_est)
    
    def backward(self, y, y_est):
        return y_est - y