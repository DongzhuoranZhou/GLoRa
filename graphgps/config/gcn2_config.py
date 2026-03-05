from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_gcn2(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument group
    cfg.gcn2 = CN()

    # then argument can be specified within the group
    cfg.gcn2.alpha = 0.1


register_config('gcn2', set_cfg_gcn2)
