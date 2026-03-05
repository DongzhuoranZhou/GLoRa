from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_lran_gnn(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument

    # example argument group
    cfg.lran_gnn = CN()

    # 'cat', 'max', 'lstm'
    cfg.lran_gnn.num_heads = 8
    cfg.lran_gnn.max_hop_func = 'linear'


register_config('lran_gnn_args', set_cfg_lran_gnn)