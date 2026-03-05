from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_dropege(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument
    cfg.dropedge = 'dropedge'

    # example argument group
    cfg.dropedge = CN()

    # then argument can be specified within the group
    cfg.dropedge.edge_dropout = 0.5



register_config('dropedge', set_cfg_dropege)
