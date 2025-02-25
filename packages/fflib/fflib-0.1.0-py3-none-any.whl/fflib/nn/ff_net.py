import torch

from torch.nn import Module
from fflib.interfaces.iff import IFF
from fflib.nn.ff_linear import FFLinear
from typing import List

class FFNet(IFF, Module):
    def __init__(self, layers: List[FFLinear], device):
        super().__init__()

        self.device = device
        self.layers: List[FFLinear] = layers

    def get_layer_count(self):
        return len(self.layers)

    def forward(self, x: torch.Tensor):
        result: List[torch.Tensor] = [] # (layer, batch_size, goodness)
        for layer in self.layers:
            # Each layer's inference returns the goodness of the layer
            # and the output of the layer to be passed to the next
            g, x = layer.goodness(x)

            if g is not None:
                result.append(g)
        
        combine_layers = sum(result)
        return combine_layers
    
    def run_train(
            self,
            x_pos: torch.Tensor,
            x_neg: torch.Tensor,
        ):

        # For each layer in the neural network
        for _, layer in enumerate(self.layers):
            layer.run_train(x_pos, x_neg)

            x_pos = layer(x_pos)
            x_neg = layer(x_neg)
