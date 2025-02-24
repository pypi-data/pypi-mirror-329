from AIScratch.NeuralNetwork.Encoders import Encoder
import numpy as np

class MinMaxEncoder(Encoder):
    def __init__(self, valmaxs, valmins):
        super().__init__()
        self.valmins = np.asarray(valmins)
        self.valmaxs = np.asarray(valmaxs)

    def encode(self, inputs):
        return (inputs - self.valmins) / (self.valmaxs - self.valmins)

    def decode(self, inputs):
        return (self.valmaxs - self.valmins) * inputs + self.valmins
        