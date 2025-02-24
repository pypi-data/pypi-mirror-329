import numpy as np
from enum import Enum
from skimage.util import view_as_windows
from AIScratch.NeuralNetwork.SpatialLayers import SpatialLayer

class PoolingType(Enum):
    MAX = 1
    AVERAGE = 2

class PoolingLayer(SpatialLayer):
    def __init__(self, k, padding, stride, channel_out, pooling_type : PoolingType):
        super().__init__(k, padding, stride, channel_out, None, "pooling_max" if pooling_type == PoolingType.MAX else "pooling_average")
        self.pooling_type = pooling_type
        if pooling_type == PoolingType.MAX:
            self.pooling = np.max
        else:
            self.pooling = np.average

    def _initialize(self, n_in, optimizer_factory, list_of_filters=None):
        self.n_in = n_in
        self.n_out = \
            (self.channel_out, int((self.n_in[1] - self.k + 2*self.padding) / self.stride) + 1,
              int((self.n_in[2] - self.k + 2*self.padding) / self.stride) + 1)
        
        print("Init pooling", self.n_in, "->", self.n_out)
        if self.pooling_type == PoolingType.MAX:
            self.argmax = np.zeros(self.n_out+(2,), dtype=int)

    def forward(self, inputs, is_training=False):
        if len(inputs) != self.channel_out:
            raise ValueError("The number of channels in the input must be equal to the number of channels in the layer.")
        if self.padding > 0:
            inputs = np.pad(inputs, ((0, 0), (self.padding, self.padding), (self.padding, self.padding)), mode='constant')

        # create all (k,k) sliding windows
        windows = view_as_windows(inputs, (1, self.k, self.k), step=(1, self.stride, self.stride))
        windows = windows.squeeze(axis=3)  # remove the last dimension

        # Max-pooling
        if self.pooling_type == PoolingType.MAX:
            self.argmax = np.argmax(windows.reshape(*windows.shape[:3], -1), axis=-1)
            self.argmax = np.unravel_index(self.argmax, (self.k, self.k))  # convert to 2D
            return np.max(windows, axis=(-1, -2))

        return np.mean(windows, axis=(-1, -2))

    def propagation(self, grad_L_z):
        if self.padding > 0: # create dX with the right padding 
            ret = np.pad(np.zeros(self.n_in), ((0, 0), (self.padding, self.padding), (self.padding, self.padding)))
        else:
            ret = np.zeros(self.n_in)
        if self.pooling_type == PoolingType.MAX:
            idx_x, idx_y = self.argmax
            i_idx, j_idx, l_idx = np.indices(grad_L_z.shape)
            ret[i_idx, j_idx * self.stride + idx_x, l_idx * self.stride + idx_y] = grad_L_z[i_idx, j_idx, l_idx]
        else:
            k_area = self.k * self.k
            for j in range(self.k):
                for l in range(self.k):
                    ret[:, j*self.stride:j*self.stride+self.k, l*self.stride:l*self.stride+self.k] += grad_L_z / k_area
        if self.padding > 0:
            return ret[:, self.padding:-self.padding, self.padding:-self.padding]
        return ret
    
    def store(self, grad_L_z):
        pass
    
    def backward(self):
        pass