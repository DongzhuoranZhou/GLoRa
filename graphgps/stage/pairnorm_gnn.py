import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.graphgym.models.layer import GATConv
from torch_geometric.graphgym.config import cfg
import torch_geometric.graphgym.models.head
from torch_geometric.graphgym.models.layer import (new_layer_config,
                                                   GeneralLayer,
                                                   GeneralMultiLayer,
                                                   BatchNorm1dNode)
from torch_geometric.graphgym.init import init_weights

import torch_geometric.graphgym.models.encoder  # noqa, register module
import torch_geometric.graphgym.register as register
from torch_geometric.graphgym.models.layer import LayerConfig, new_layer_config
from torch_geometric.nn.norm.pair_norm import PairNorm


def GNNLayer(dim_in, dim_out, has_act=True):
    """
    Wrapper for a GNN layer

    Args:
        dim_in (int): Input dimension
        dim_out (int): Output dimension
        has_act (bool): Whether has activation function after the layer

    """
    return GeneralLayer(
        cfg.gnn.layer_type,
        layer_config=new_layer_config(dim_in, dim_out, 1, has_act=has_act,
                                      has_bias=False, cfg=cfg))


class Pairnorm_GNNStackStage(nn.Module):
    """
    Simple Stage that stack GNN layers

    Args:
        dim_in (int): Input dimension
        dim_out (int): Output dimension
        num_layers (int): Number of GNN layers
    """

    def __init__(self, dim_in, dim_out, num_layers):
        super(Pairnorm_GNNStackStage, self).__init__()
        self.num_layers = num_layers
        for i in range(num_layers):
            if cfg.gnn.stage_type == 'skipconcat':
                d_in = dim_in if i == 0 else dim_in + i * dim_out
            else:
                d_in = dim_in if i == 0 else dim_out
            layer = GNNLayer(d_in, dim_out)
            self.add_module('layer{}'.format(i), layer)

    def forward(self, batch):
        """"""
        for i, layer in enumerate(self.children()):
            # x = batch.x
            batch = layer(batch)
            # if cfg.gnn.stage_type == 'skipsum':
            #     batch.x = x + batch.x
            # elif cfg.gnn.stage_type == 'skipconcat' and \
            #         i < self.num_layers - 1:
            #     batch.x = torch.cat([x, batch.x], dim=1)
        if cfg.gnn.l2norm:
            batch.x = F.normalize(batch.x, p=2, dim=-1)
        return batch


class GeneralLayer(nn.Module):
    """
    General wrapper for layers

    Args:
        name (string): Name of the layer in registered :obj:`layer_dict`
        dim_in (int): Input dimension
        dim_out (int): Output dimension
        has_act (bool): Whether has activation after the layer
        has_bn (bool):  Whether has BatchNorm in the layer
        has_l2norm (bool): Wheter has L2 normalization after the layer
        **kwargs (optional): Additional args
    """

    def __init__(self, name, layer_config: LayerConfig, **kwargs):
        super(GeneralLayer, self).__init__()
        self.has_l2norm = layer_config.has_l2norm
        has_bn = layer_config.has_batchnorm
        layer_config.has_bias = True
        self.layer = register.layer_dict[name](layer_config, **kwargs)

        layer_wrapper = []

        # if has_pn: # before activation function
        layer_wrapper.append(
            PairNorm(scale=cfg.pairnorm.scale, scale_individually=cfg.pairnorm.scale_individually,
                     eps=cfg.pairnorm.eps))
        # self.pn = PairNorm(scale=cfg.pairnorm.scale, scale_individually=cfg.pairnorm.scale_individually,
        #              eps=cfg.pairnorm.eps)
        if has_bn:
            layer_wrapper.append(
                nn.BatchNorm1d(layer_config.dim_out,
                               eps=layer_config.bn_eps,
                               momentum=layer_config.bn_mom))
        if layer_config.dropout > 0:
            layer_wrapper.append(
                nn.Dropout(p=layer_config.dropout,
                           inplace=layer_config.mem_inplace))
        if layer_config.has_act:
            layer_wrapper.append(register.act_dict[layer_config.act])
        self.post_layer = nn.Sequential(*layer_wrapper)

    def forward(self, batch):
        batch = self.layer(batch)
        if isinstance(batch, torch.Tensor):
            # batch.x = self.pn(x=batch.x)
            batch = self.post_layer(batch)
            if self.has_l2norm:
                batch = F.normalize(batch, p=2, dim=1)
        else:
            # batch.x = self.pn(x=batch.x)
            batch.x = self.post_layer(batch.x)
            if self.has_l2norm:
                batch.x = F.normalize(batch.x, p=2, dim=1)
        return batch


stage_dict = {
    'pairnorm_gnn': Pairnorm_GNNStackStage,
}

register.stage_dict = {**register.stage_dict, **stage_dict}
