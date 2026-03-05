import torch
import torch.nn as nn
from torch_geometric.nn.conv import GATConv
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.register import register_layer
from torch_geometric.graphgym.models.layer import LayerConfig

class Custom_GATconv(nn.Module):
    """
    Graph Attention Network (GAT) layer

    This one allows a custom edge_index to be passed in.
    """
    def __init__(self, layer_config: LayerConfig, **kwargs):
        super().__init__()
        self.model = GATConv(layer_config.dim_in, layer_config.dim_out,
                             heads=cfg.lran_gnn.num_heads,  # Number of attention heads, default is 1
                             concat=True,  # Whether to concatenate the heads' outputs
                             dropout=kwargs.get('dropout', 0.0),  # Dropout rate, default is 0.0
                             add_self_loops=False,
                             bias=layer_config.has_bias)

    def forward(self, batch, x, edge_index):
        x = self.model(x, edge_index)
        return x

register_layer('custom_gatconv', Custom_GATconv)
