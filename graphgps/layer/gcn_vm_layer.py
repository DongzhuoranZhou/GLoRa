import torch
import torch.nn as nn
from torch.nn import Parameter
from torch_geometric.nn.conv import MessagePassing

from torch_geometric.nn.inits import glorot, zeros
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.register import register_layer

import torch_geometric as pyg
from torch_geometric.graphgym.models.layer import LayerConfig

class VNGCNconv(nn.Module):
    """
    Graph Convolutional Network (GCN) layer

    This one allows a custom edge_index, edge_attr to be passed in
    """
    def __init__(self, layer_config: LayerConfig, **kwargs):
        super().__init__()
        self.model = pyg.nn.GCNConv(layer_config.dim_in, layer_config.dim_out,
                                    bias=layer_config.has_bias)
    def reset_parameters(self):
        self.model.reset_parameters()
    def forward(self, batch,edge_index,edge_attr):
        batch.x = self.model(x=batch.x, edge_index=edge_index,edge_weight=edge_attr)
        # batch.x = nn.ReLU()(batch.x)

        return batch

register_layer('vn_gcn', VNGCNconv)