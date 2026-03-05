
import torch_geometric.graphgym.register as register
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.register import register_network

from torch import nn

from functools import partial

from .mixhop_layer import MixHopConv,ListModule  # from torch geometric
from torch_geometric.graphgym.models.gnn import FeatureEncoder, GNNPreMP


class MixHopGCN_Torch(nn.Module):
    r'''
    encode
    pre_mp
    gnn
    post_mp
    '''

    def __init__(self, dim_in, dim_out):
        super().__init__()

        pre_mp_dim_in = dim_in
        if cfg.mixhop_args.powers != None:
            cfg.mixhop_args.layers = [cfg.gnn.dim_inner] * len(cfg.mixhop_args.powers)
        else:
            print(
                'Warning: P parameter not set for MixHop; node encoder and MixHop layer dimensionalities will be inconsistent.')
        assert len(set(cfg.mixhop_args.layers)) == 1  # first layer has same dimensionality for each adj power
        dim_in = cfg.mixhop_args.layers[0]
        # Encode node features.
        self.encoder = FeatureEncoder(dim_in)
        dim_in = self.encoder.dim_in

        # Pre-mp layers.
        if cfg.gnn.layers_pre_mp > 0:
            self.pre_mp = GNNPreMP(
                pre_mp_dim_in, cfg.gnn.dim_inner, cfg.gnn.layers_pre_mp)
            dim_in = cfg.gnn.dim_inner
        else:
            self.pre_mp = nn.Identity()

        assert cfg.gnn.dim_inner == dim_in, \
            "The inner and hidden dims must match."

        feature_number = dim_in  # node feature dim
        class_number = dim_out  # maybe? or whatever the output is

        self.args = cfg.mixhop_args
        self.args.dropout = cfg.gnn.dropout
        self.feature_number = feature_number
        self.class_number = class_number
        self.setup_layer_structure()

        save_num_post_mp_layers = cfg.gnn.layers_post_mp
        if cfg.gnn.layers_post_mp > 1:  # if there are multiple post-mp layers we want them to have inner dim d, not P*d
            self.pre_post_mp = nn.Sequential(nn.Linear(cfg.gnn.dim_inner * cfg.mixhop_args.max_P,
                                                       cfg.gnn.dim_inner, bias=True),
                                             nn.ReLU())

            cfg.gnn.layers_post_mp -= 1
            head_dim_in = cfg.mixhop_args.layers[0]
        else:
            # head_dim_in = sum(cfg.mixhop_args.layers)
            head_dim_in = sum(cfg.mixhop_args.layers)

        GNNHead = register.head_dict[cfg.gnn.head]
        from graphgps.drew_utils import get_task_id
        if get_task_id() == 'pcqm':
            kwargs = dict(mixhop_dims=(sum(cfg.mixhop_args.layers), cfg.mixhop_args.layers[
                0]))  # want final layer in InductiveEdgeHead to be Pd * d, not Pd*Pd
        else:
            kwargs = {}
        self.post_mp = GNNHead(dim_in=head_dim_in, dim_out=dim_out, **kwargs)
        cfg.gnn.layers_post_mp = save_num_post_mp_layers

    def forward(self, batch):

        batch = self.encoder(batch)
        batch = self.pre_mp(batch)

        for t in range(cfg.gnn.layers_mp):
            batch.x = self.layers[t](batch.x, batch.edge_index)
            if cfg.gnn.batchnorm: batch.x = self.batchnorm[t](batch.x)
            batch.x = nn.ReLU()(batch.x)

        if cfg.gnn.layers_post_mp > 1: batch.x = self.pre_post_mp(batch.x)
        batch = self.post_mp(batch)
        return batch

    def setup_layer_structure(self):
        if cfg.gnn.batchnorm:
            bn = partial(nn.BatchNorm1d, sum(self.args.layers), eps=cfg.bn.eps, momentum=cfg.bn.mom)
            self.batchnorm = [bn()]
        first_layer = MixHopConv(self.feature_number, self.args.layers[0], [0, 1, 2], add_self_loops=True)
        self.layers = [first_layer]
        for t in range(cfg.gnn.layers_mp):
            self.layers.append(MixHopConv(sum(self.args.layers), self.feature_number, [0, 1, 2], add_self_loops=True))
            if cfg.gnn.batchnorm: self.batchnorm.append(bn())
        self.layers = nn.ModuleList(self.layers)
        if cfg.gnn.batchnorm: self.batchnorm = nn.ModuleList(self.batchnorm)


register_network('mixhop_gcn', MixHopGCN_Torch)
