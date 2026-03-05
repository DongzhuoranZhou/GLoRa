import torch
import torch.nn as nn
import torch.nn.functional as F

from torch_geometric.graphgym.config import cfg

import torch_geometric.graphgym.models.encoder  # noqa, register module
import torch_geometric.graphgym.register as register
from torch_geometric.graphgym.models.gnn import GNNLayer
from torch_geometric.utils import dropout_adj
from torch_geometric.graphgym.register import register_stage


class DropEdge_GNNStackStage(nn.Module):
    """
    Simple Stage that stack GNN layers

    Args:
        dim_in (int): Input dimension
        dim_out (int): Output dimension
        num_layers (int): Number of GNN layers
    """

    def __init__(self, dim_in, dim_out, num_layers):
        super(DropEdge_GNNStackStage, self).__init__()
        self.num_layers = num_layers
        for i in range(num_layers):

            d_in = dim_in if i == 0 else dim_out
            layer = GNNLayer(d_in, dim_out)
            self.add_module('layer{}'.format(i), layer)

    def forward(self, batch):
        """"""
        for i, layer in enumerate(self.children()):
            x, edge_index = batch.x, batch.edge_index
            batch.edge_index, _ = dropout_adj(edge_index, p=cfg.dropedge.edge_dropout,
                                              force_undirected=False)  # , training=self.training
            batch = layer(batch)
        if cfg.gnn.l2norm:
            batch.x = F.normalize(batch.x, p=2, dim=-1)
        return batch


register_stage('dropedge_gnn', DropEdge_GNNStackStage)
