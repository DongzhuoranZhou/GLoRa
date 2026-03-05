
import torch.nn as nn
import torch_geometric as pyg


import torch_geometric.graphgym.register as register
from torch_geometric.graphgym.models.layer import LayerConfig, new_layer_config
from torch_geometric.graphgym.config import cfg


class GCN2Conv(nn.Module):
    """
    GraphSAGE Conv layer
    """

    def __init__(self, layer_config: LayerConfig, **kwargs):
        super(GCN2Conv, self).__init__()
        self.model = pyg.nn.GCN2Conv(
            channels=layer_config.dim_in,
            alpha=cfg.gcn2.alpha,
            # bias=layer_config.has_bias
        )

    def forward(self, batch):
        batch.x = self.model(x=batch.x, x_0=batch.x_0, edge_index=batch.edge_index)
        return batch


class SGConv(nn.Module):
    """
    GraphSAGE Conv layer
    """

    def __init__(self, layer_config: LayerConfig, **kwargs):
        super(SGConv, self).__init__()
        self.model = pyg.nn.SGConv(
            layer_config.dim_in,
            layer_config.dim_out,
            bias=layer_config.has_bias)

    def forward(self, batch):
        batch.x = self.model(batch.x, batch.edge_index)
        return batch


class APPNP(nn.Module):
    """
    GraphSAGE Conv layer
    """

    def __init__(self, layer_config: LayerConfig, **kwargs):
        super(APPNP, self).__init__()
        self.model = pyg.nn.APPNP(
            K=cfg.appnp.K,
            alpha=cfg.appnp.alpha,
            # bias=layer_config.has_bias
        )

    def forward(self, batch):
        batch.x = self.model(batch.x, batch.edge_index)
        return batch


layer_dict = {
    'gcn2conv': GCN2Conv,  # gcn2_gnn
    'sgconv': SGConv,  # stack
    'appnpconv': APPNP,  # stack
}

register.layer_dict = {**register.layer_dict, **layer_dict}
