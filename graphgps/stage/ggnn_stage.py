
import torch.nn as nn

from torch_geometric.nn.conv.gated_graph_conv import GatedGraphConv
from torch_geometric.graphgym.register import register_stage



class Gated_GNN_Stack_Stage(nn.Module):
    """GatedGCN layer.
    The gated graph convolution operator from the `"Gated Graph Sequence Neural Networks" <https://arxiv.org/abs/1511.05493>`_ paper.

    Generate a Wrapper for the ResGatedGraphConv layer from torch_geometric.nn.conv for GraphGym.
    from torch_geometric.graphgym.models.layer import GeneralLayer, this is the wrapper for GraphGym Layer.

    Two points to note:
    1. The `forward` method should take in `batch` as the first argument and return `batch`. Rather than taking in `x`, `edge_index`, `edge_attr` as arguments.
    2. the initialization of the model should be by passing `layer_config` as the first argument. Rather than passing the individual arguments.
    """
    def __init__(self, dim_in, dim_out, num_layers):
        super(Gated_GNN_Stack_Stage, self).__init__()
        self.model = GatedGraphConv(out_channels=dim_out, num_layers=num_layers)

    def forward(self, batch):
        batch.x = self.model(batch.x, batch.edge_index)
        return batch
# register_layer('ggnn', GatedGraphConv_Torch_Geometric_GymLayer)
register_stage('ggnn', Gated_GNN_Stack_Stage)
