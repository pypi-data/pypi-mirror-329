from enum import Enum
from AIScratch.NeuralNetwork.Layers.layer import Layer
from AIScratch.NeuralNetwork.Layers.dense import DenseLayer
from AIScratch.NeuralNetwork.Layers.dropout import DropoutLayer

layer_set = {
    "dense": DenseLayer,
    "dropout": DropoutLayer
}

