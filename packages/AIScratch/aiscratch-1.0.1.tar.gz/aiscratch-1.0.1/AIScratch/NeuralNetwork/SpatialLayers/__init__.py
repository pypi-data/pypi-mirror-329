from AIScratch.NeuralNetwork.SpatialLayers.spatial_layer import SpatialLayer
from AIScratch.NeuralNetwork.SpatialLayers.pooling import PoolingLayer, PoolingType
from AIScratch.NeuralNetwork.SpatialLayers.flatten import FlattenLayer
from AIScratch.NeuralNetwork.SpatialLayers.conv2d import Conv2DLayer

spatiallayer_set = {
    "conv2d": Conv2DLayer,
    "flatten": FlattenLayer,
    "pooling": PoolingLayer
}
