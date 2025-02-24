import numpy as np
from AIScratch.NeuralNetwork.Layers import Layer
from AIScratch.NeuralNetwork.Perceptron import Perceptron

class DenseLayer(Layer):
    def __init__(self, n_out, activation_function):
        super().__init__(n_out, activation_function, "dense")

    def _initialize(self, n_in, optimizer_factory, list_of_weights = []):
        self.n_in = n_in
        self.optimizer = optimizer_factory(self.n_in, self.n_out)
        self.grad_L_w = np.zeros((self.n_out, n_in))
        self.grad_L_b = np.zeros(self.n_out)
        self.batch_size = 0
        for i in range(self.n_out):
            if len(list_of_weights) == 0 :
                weights = [self.activation_function.weight_initialize(n_in, self.n_out) for _ in range(n_in)]
                bias = np.random.random() * 0.2 - 0.1
            else:
                weights = list_of_weights[i][:-1]
                bias = list_of_weights[i][-1]
            self.neurons.append(Perceptron(weights, bias))

    def forward(self, inputs, is_training = False):
        self.last_inputs = inputs.copy() 
        self.last_sums = np.array([neuron.forward(self.last_inputs) for neuron in self.neurons])
        self.last_activations = self.activation_function.forward(self.last_sums)
        return self.last_activations
    
    def propagation(self, grad_L_z):
        previous_weights = np.array([neuron.weights for neuron in self.neurons]) # create matrix of previus layer weights (for next layer its our current one)
        return np.dot(grad_L_z, previous_weights) # compute next layer errors
    
    def store(self, grad_L_z):
        self.batch_size += 1
        grad_L_w = self.optimizer.store(grad_L_z, self.last_inputs)
        self.grad_L_w += grad_L_w 
        self.grad_L_b += grad_L_z
    
    def backward(self):
        learning_rates, weighted_errors, biais_update = self.optimizer.optimize(
            self.grad_L_w / self.batch_size, self.grad_L_b / self.batch_size
        )
        for i in range(self.n_out):
            self.neurons[i].backward(learning_rates[i], weighted_errors[i], biais_update[i])
        # update for next batch
        self.grad_L_w.fill(0)
        self.grad_L_b.fill(0)
        self.batch_size = 0