import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.register import register_stage
import torch
from .example import GNNLayer
from torch_geometric.graphgym.models.gnn import GNNLayer
from torch_geometric.nn.models.jumping_knowledge import JumpingKnowledge
from torch.nn import Linear

class JK_GNN(nn.Module):
    """
    Simple Stage that stack GNN layers
# https://github.com/pyg-team/pytorch_geometric/blob/master/benchmark/kernel/gin.py#L54
    Args:
        dim_in (int): Input dimension
        dim_out (int): Output dimension
        num_layers (int): Number of GNN layers
    """

    def __init__(self, dim_in, dim_out, num_layers):
        super(JK_GNN, self).__init__()
        self.num_layers = num_layers
        self.mode = cfg.jumpknowledge.mode


        for i in range(num_layers):
            d_in = dim_in if i == 0 else dim_out
            layer = GNNLayer(d_in, dim_out)
            self.add_module('layer{}'.format(i), layer)

        self.jump = JumpingKnowledge(mode=self.mode)  # TODO
        if self.mode == 'cat':
            self.lin1 = Linear((num_layers + 1) * dim_out, dim_out)
        else:
            self.lin1 = Linear(dim_out, dim_out)
    def forward(self, batch):
        """"""
        xs = [batch.x]
        for i, layer in enumerate(self.children()):
            if type(layer) in (JumpingKnowledge, Linear):
                continue
            batch = layer(batch)
            xs += [batch.x]
        x = self.jump(xs)
        batch.x = self.lin1(x)
        if cfg.gnn.l2norm:
            batch.x = F.normalize(batch.x, p=2, dim=-1)
        return batch


register_stage('jk_gnn', JK_GNN)
