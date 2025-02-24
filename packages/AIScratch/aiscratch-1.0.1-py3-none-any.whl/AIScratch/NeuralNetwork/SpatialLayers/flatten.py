from AIScratch.NeuralNetwork.SpatialLayers import SpatialLayer

class FlattenLayer(SpatialLayer):
    def __init__(self):
        super().__init__(0, 0, 0, 0, None, "flatten")

    def _initialize(self, n_in, optimizer_factory, list_of_filters=None):
        self.n_in = n_in
        self.n_out = n_in[0]*n_in[1]*n_in[2]
        print("Init flatten", self.n_in, "->", self.n_out)

    def forward(self, inputs, is_training=False):
        return inputs.flatten()
    
    def propagation(self, grad_L_z):
        return grad_L_z.reshape(self.n_in)
            
    def store(self, grad_L_z):
        pass
    
    def backward(self):
        pass