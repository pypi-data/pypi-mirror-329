import numpy as np
from scipy.signal import correlate, correlate2d
from AIScratch.NeuralNetwork.SpatialLayers import SpatialLayer
from AIScratch.NeuralNetwork.ActivationFunctions import ActivationFunction

class Conv2DLayer(SpatialLayer):
    def __init__(self, k, padding, stride, channel_out, activation_function : ActivationFunction):
        super().__init__(k, padding, stride, channel_out, activation_function, "conv2d")

    def _initialize(self, n_in, optimizer_factory, list_of_filters=None):
        # size init
        self.n_in = n_in # n channels in of size h x w
        self.n_out = \
            (self.channel_out, int((self.n_in[1] - self.k + 2*self.padding) / self.stride) + 1,
              int((self.n_in[2] - self.k + 2*self.padding) / self.stride) + 1)
        print("Init conv", self.n_in, "->", self.n_out)
        self.filter_size = (self.channel_out, self.n_in[0], self.k, self.k)
        # optimizer
        self.optimizer = optimizer_factory((self.k, self.k), (self.channel_out, self.n_in[0]))
        # batch init
        self.batch_size = 0
        self.grad_L_w = np.zeros(self.filter_size)  # Weights variations
        self.grad_L_b = np.zeros(self.channel_out) # Biases variations
        # weights init
        if list_of_filters is None:
            self.filters = np.array([self.activation_function.weight_initialize(self.n_in[0] * self.k * self.k, self.n_out[0] * self.k * self.k) for _ in np.ndindex(self.filter_size)]).reshape(self.filter_size) # c channel out for n channel in and filter of size k x k
            self.bias = np.zeros(self.channel_out)
        else:
            self.filters = list_of_filters[0]
            self.bias = list_of_filters[1]
        self.flipped_filters = np.flip(self.filters, axis=(2, 3))

    def propagation(self, grad_L_z):
        if self.padding > 0: # create dX with the right padding 
            dX = np.pad(np.zeros(self.n_in), ((0, 0), (self.padding, self.padding), (self.padding, self.padding)))
        else:
            dX = np.zeros(self.n_in)
        # compute the impact of each out pixel for the in pixels
        for c_out in range(self.n_out[1]):
            for c_in in range(self.n_out[2]):
                #! stride and filter size is taken into account here
                h_start = c_out * self.stride
                h_end = h_start + self.k
                w_start = c_in * self.stride
                w_end = w_start + self.k
                # update variation of inputs at the right place
                dX[:, h_start:h_end, w_start:w_end] += np.sum(
                    self.flipped_filters.reshape(self.n_out[0], self.n_in[0], self.k, self.k) * grad_L_z[:, c_out, c_in].reshape(self.n_out[0], 1, 1, 1), axis=0
                )
        # return using the right padding
        if self.padding > 0:
            return dX[:, self.padding:-self.padding, self.padding:-self.padding]
        return dX

    def forward(self, inputs, is_training=False):
        if self.padding > 0:
            self.last_inputs = np.pad(inputs, ((0, 0), (self.padding, self.padding), (self.padding, self.padding)), mode='constant', constant_values=0)
        else:
            self.last_inputs = inputs
        self.last_sums = np.zeros(self.n_out)
        for c_out in range(self.n_out[0]):  # filter iterations
            for c_in in range(self.n_in[0]):  # channel in iterations
                self.last_sums[c_out] += correlate(self.last_inputs[c_in], self.filters[c_out, c_in], mode='valid')[::self.stride, ::self.stride]
            self.last_sums[c_out] += self.bias[c_out]
        self.last_activations = self.activation_function.forward(self.last_sums)
        return self.last_activations # n channels of size h' x w'
            
    def store(self, grad_L_z):   
        # grad_L_z is n channels of size h' x w' 
        self.grad_L_b += np.sum(grad_L_z, axis=(1, 2)) # grad_L_b is c_out in lengths
        for c_out in range(self.n_out[0]):  # filter iterations
            for c_in in range(self.n_in[0]):  # channel in iterations
                self.grad_L_w[c_out, c_in] += correlate(
                    self.last_inputs[c_in], grad_L_z[c_out], mode='valid')[::self.stride, ::self.stride]
        self.batch_size += 1
    
    def backward(self):
        learning_rates, weighted_errors, biais_update = self.optimizer.optimize(
            self.grad_L_w / self.batch_size, self.grad_L_b / self.batch_size
        )
        self.filters -= learning_rates * weighted_errors
        self.flipped_filters = np.flip(self.filters, axis=(2, 3))
        self.bias -= biais_update
        # update for next batch
        self.grad_L_w.fill(0)
        self.grad_L_b.fill(0)
        self.batch_size = 0