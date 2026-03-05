import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.register import register_stage
import torch
from .example import GNNLayer
from torch_geometric.graphgym.models.gnn import GNNLayer





class DIGL_GNN(nn.Module):
    """
    Simple Stage that stack GNN layers

    Args:
        dim_in (int): Input dimension
        dim_out (int): Output dimension
        num_layers (int): Number of GNN layers
    """
    def __init__(self, dim_in, dim_out, num_layers):
        super(DIGL_GNN, self).__init__()
        self.num_layers = num_layers
        for i in range(num_layers):
            d_in = dim_in if i == 0 else dim_out
            layer = GNNLayer(d_in, dim_out)
            self.add_module('layer{}'.format(i), layer)

    def forward(self, batch):
        """"""
        for i, layer in enumerate(self.children()):
            batch = layer(batch)
        if cfg.gnn.l2norm:
            batch.x = F.normalize(batch.x, p=2, dim=-1)
        return batch


register_stage('digl_gnn', DIGL_GNN)

