from yacs.config import CfgNode as CN

from torch_geometric.graphgym.register import register_config


def set_cfg_jknet(cfg):
    r'''
    This function sets the default config value for customized options
    :return: customized configuration use by the experiment.
    '''

    # ----------------------------------------------------------------------- #
    # Customized options
    # ----------------------------------------------------------------------- #

    # example argument

    # example argument group
    cfg.jumpknowledge = CN()

    # 'cat', 'max', 'lstm'
    cfg.jumpknowledge.mode = 'cat'


register_config('jknet_args', set_cfg_jknet)