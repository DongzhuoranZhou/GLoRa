import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.register import register_stage
from .example import GNNLayer



class FOSR_GNNStackStage(nn.Module):
    """
    Simple Stage that stack GNN layers
    copied from torch_geometric
    Args:
        dim_in (int): Input dimension
        dim_out (int): Output dimension
        num_layers (int): Number of GNN layers
    """
    def __init__(self, dim_in, dim_out, num_layers):
        super(FOSR_GNNStackStage, self).__init__()
        self.num_layers = num_layers
        for i in range(num_layers):
            d_in = dim_in if i == 0 else dim_out
            layer = GNNLayer(d_in, dim_out)
            self.add_module('layer{}'.format(i), layer)

    def forward(self, batch):
        """
        Last layer is fully connected layer
        Args:
            batch:

        Returns:

        """
        # every_layer = True
        A_fosr = batch.edge_index[:, batch.edge_attr == -20]
        for i, layer in enumerate(self.children()):
            x = batch.x
            batch = layer(batch,x,A_fosr) # TODO
        if cfg.gnn.l2norm:
            batch.x = F.normalize(batch.x, p=2, dim=-1)
        return batch

register_stage('fosr_gnn', FOSR_GNNStackStage)

