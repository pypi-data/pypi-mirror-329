import numpy as np
from enum import Enum
from typing import Callable, Any, Union
from AIScratch.NeuralNetwork.Perceptron import Perceptron
from AIScratch.NeuralNetwork.ActivationFunctions import ActivationFunction, activation_set
from AIScratch.NeuralNetwork.Optimizers import Optimizer
from AIScratch.NeuralNetwork.ErrorFunctions import ErrorFunction
from AIScratch.NeuralNetwork.Layers import Layer, layer_set
from AIScratch.NeuralNetwork.SpatialLayers import SpatialLayer, PoolingType, spatiallayer_set

class MLP():
    def __init__(self, input_number : int, layers : list[Union[Layer, SpatialLayer]], error_function : ErrorFunction, optimizer_factory : Callable[[int, int], Optimizer], batch_size = 1):
        self.input_number = input_number
        self.optimizer_factory = optimizer_factory
        self.layers : list[Union[Layer, SpatialLayer]] = layers
        self.error_function = error_function
        self.batch_size = batch_size
        self.batch_counter = 0
        self.__freeze_layers = -1
        self.__initialize()

    def __initialize(self):
        prev_size = self.input_number
        for layer in self.layers:
            layer._initialize(prev_size, self.optimizer_factory)
            prev_size = layer.n_out

    def set_freeze_layer(self, num : int):
        self.__freeze_layers = num if isinstance(num, int) and num > 0 else -1

    def unfreeze_layer(self):
        self.set_freeze_layer(-1)

    def forward(self, inputs, is_training = False):
        outputs = np.asarray(inputs)
        for layer in self.layers:
            outputs = layer.forward(outputs, is_training)
        return outputs
    
    def __errors(self, name_last_layer, expected_outputs, outputs):
        if name_last_layer == "softmax":
            return outputs - expected_outputs
        return self.error_function.backward(expected_outputs, outputs)
    
    def __gradient(self, layer : Layer, errors):
        if layer.name.startswith("pooling") or layer.name == "flatten":
            return errors
        if layer.activation_function.name == "softmax":
            gradients = 1
        else:
            gradients = layer.activation_function.backward(layer.last_sums) # f'p(z) #! modified without test
        grad_L_z = errors * gradients # dL/dz = dL/dy * f'p(z)
        layer.store(grad_L_z) # store gradient
        return grad_L_z

    def backward(self, inputs, expected_outputs):
        expected_outputs = np.asarray(expected_outputs)
        inputs = np.asarray(inputs)
        outputs = self.forward(inputs, is_training=True) # all neurons stores the inputs and all layers store activations
        errors = self.__errors(self.layers[-1].activation_function.name, expected_outputs, outputs) # compute errors for last layer
        grad_L_z = np.zeros_like(errors)
        self.batch_counter += 1
        for p in reversed(range(len(self.layers))): # each layer should compute gradient for itself and error for next
            if p < self.__freeze_layers: # allow to learn only the last layers
                break
            # current layer computation
            layer = self.layers[p] # layer p
            grad_L_z = self.__gradient(layer, errors)
            if self.batch_counter == self.batch_size:
                layer.backward()
            errors = layer.propagation(grad_L_z) # compute errors for next layer
        if self.batch_counter == self.batch_size:
            self.batch_counter = 0

    def extract(self, file_path : str):
        with open(file_path, "w") as f:
            f.write(f"MLP : {self.input_number}\n")
            for layer in self.layers:
                if layer.name == "flatten":
                    f.write(f"*-*{layer.name}\n")
                    continue
                if layer.is_spatial:
                    f.write(f"*-*{layer.name}//{layer.k}//{layer.padding}//{layer.stride}//{layer.channel_out}")
                    if layer.name.startswith("pooling"):
                        f.write("\n")
                        continue
                    f.write(f"//{layer.activation_function.name}\n")
                    for i in range(len(layer.filters)):
                        filter = layer.filters[i]
                        f.write("|".join(map(str, filter.flatten())))
                        f.write(f"|{layer.bias[i]}\n")
                    continue
                f.write(f"*-*{layer.name}//{layer.n_out}//{layer.activation_function.name}\n")
                for neuron in layer.neurons:
                    f.write("|".join(map(str, neuron.weights)))
                    f.write("|" + str(neuron.bias) + "\n")

    def load(self, file_path : str):
        self.layers = []
        with open(file_path, "r") as f:
            lines = f.readlines()
        layer_data = None
        prev_size = self.input_number
        list_of_weights = []
        for i in range(len(lines) + 1):
            #!----- quick introduction to compare input size
            if i == 0 and prev_size != tuple(map(int, lines[i].strip()[7:-1].split(', '))):
                print(f"*-* Error while loading the file. Not same input size (expected : {tuple(map(int, lines[i].strip()[7:-1].split(', ')))}).")
                break
            if i == 0:
                continue
            #!----- layer header
            if i == len(lines) or lines[i].startswith("*-*"): 
                if layer_data != None: # this means that we already encountered a layer, so we add last layer and then start again
                    if layer_data["spatial"] == False:
                        self.layers.append(
                            layer_set[layer_data["name"]](
                                layer_data["n_out"], 
                                activation_set[layer_data["activation_function"]]
                            )
                        )
                    else:
                        if layer_data["name"] == "flatten":
                            self.layers.append(spatiallayer_set[layer_data["name"]]())
                        elif layer_data["name"] == "conv2d":
                            self.layers.append(spatiallayer_set[layer_data["name"]](
                                layer_data["k"], layer_data["padding"], layer_data["stride"], layer_data["channel_out"],
                                activation_set[layer_data["activation_function"]]
                            ))
                        else:
                            self.layers.append(spatiallayer_set[layer_data["name"].split("_")[0]](
                                layer_data["k"], layer_data["padding"], layer_data["stride"], layer_data["channel_out"],
                                PoolingType.MAX if layer_data["name"] == "pooling_max" else PoolingType.AVERAGE
                            ))
                    self.layers[-1]._initialize(prev_size, self.optimizer_factory, list_of_weights)
                    prev_size = self.layers[-1].n_out
            #!----- layer header
            if i == len(lines) or lines[i].startswith("*-*"): 
                if i == len(lines): # get out of the loop
                    break
                layer_data = {}
                layer_txt = lines[i][3:].strip().split("//")
                layer_data["name"] = layer_txt[0]
                index = 0
                if len(layer_txt) == 3:
                    layer_data["spatial"] = False
                    layer_data["n_out"] = int(layer_txt[1])
                    layer_data["activation_function"] = layer_txt[2]
                    list_of_weights = np.zeros((layer_data["n_out"], prev_size + 1))
                else:
                    layer_data["spatial"] = True
                    if len(layer_txt) > 1:
                        layer_data["k"] = int(layer_txt[1])
                        layer_data["padding"] = int(layer_txt[2])
                        layer_data["stride"] = int(layer_txt[3])
                        layer_data["channel_out"] = int(layer_txt[4])
                    if len(layer_txt) == 6:
                        layer_data["activation_function"] = layer_txt[5]
                        list_of_weights = [np.zeros((layer_data["channel_out"], prev_size[0], layer_data["k"], layer_data["k"])), np.zeros(layer_data["channel_out"])]
                continue
            #!----- weights
            weights_val = np.array(list(map(float, lines[i].strip().split("|"))))
            if layer_data["spatial"]:
                list_of_weights[0][index] = weights_val[:-1].reshape((prev_size[0], layer_data["k"], layer_data["k"]))
                list_of_weights[1][index] = weights_val[-1]
            else:
                list_of_weights[index] = weights_val
            index += 1

    def __repr__(self):
        return f"{self.input_number} : " + " -> ".join(map(lambda x : x.name, self.layers))


