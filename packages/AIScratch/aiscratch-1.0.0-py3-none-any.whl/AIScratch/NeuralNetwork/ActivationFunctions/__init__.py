from AIScratch.NeuralNetwork.ActivationFunctions.function import ActivationFunction
from AIScratch.NeuralNetwork.ActivationFunctions.linear import Linear
from AIScratch.NeuralNetwork.ActivationFunctions.relu import ReLU
from AIScratch.NeuralNetwork.ActivationFunctions.treshold import Treshold
from AIScratch.NeuralNetwork.ActivationFunctions.sigmoide import Sigmoïde
from AIScratch.NeuralNetwork.ActivationFunctions.softmax import Softmax

activation_set = {
    "linear": Linear(),
    "relu": ReLU(),
    "treshold": Treshold(),
    "sigmoïde": Sigmoïde(),
    "softmax": Softmax()
}